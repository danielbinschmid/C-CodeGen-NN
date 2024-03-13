import tvm 
from tvm.relay import frontend
import onnx 
from tvm.relay.backend import Runtime
from tvm.micro import export_model_library_format
from tvm.relay.op.contrib import cmsisnn
import argparse

# parse args ------
parser = argparse.ArgumentParser()
parser.add_argument('-out_tar', help='tar file output path')
parser.add_argument('-onnx_model', help='input onnx model')
args = parser.parse_args()

ONNX_MODEL_PATH = args.onnx_model
TAR_PATH        = args.out_tar

print(ONNX_MODEL_PATH)
print(TAR_PATH)
# -----------------

def microTVM():
    # configuration ------------------------------

    # We can use TVM native schedules or rely on the CMSIS-NN kernels using TVM Bring-Your-Own-Code (BYOC) capability.
    USE_CMSIS_NN = True

    # USMP (Unified Static Memory Planning) performs memory planning of all tensors holistically to achieve best memory utilization
    DISABLE_USMP = False

    # Use the C runtime (crt)
    RUNTIME = Runtime("crt")

    # We define the target by passing the board name to `tvm.target.target.micro`.
    # If your board is not included in the supported models, you can define the target such as:
    # TARGET = tvm.target.Target("c -keys=arm_cpu,cpu -mcpu=cortex-m4")
    # TARGET = tvm.target.target.micro("stm32l4r5zi")
    TARGET = tvm.target.Target("c -device=riscv64")
    # --------------------------------------------

    # convert onnx to relay module ---------------
    onnx_model_path = ONNX_MODEL_PATH
    onnx_model = onnx.load(onnx_model_path)
    
    relay_mod, params = frontend.from_onnx(onnx_model, freeze_params=True)
    print("built relay_mod")
    # --------------------------------------------

    # lower relay module -------------------------
    
    # Use the AOT executor rather than graph or vm executors. Use unpacked API and C calling style.
    EXECUTOR = tvm.relay.backend.Executor(
        "aot", {"unpacked-api": True, "interface-api": "c", "workspace-byte-alignment": 8}
    )

    # Now, we set the compilation configurations and compile the model for the target:
    config = {"tir.disable_vectorize": True}
    if USE_CMSIS_NN:
        config["relay.ext.cmsisnn.options"] = {"mcpu": TARGET.mcpu}
    if DISABLE_USMP:
        config["tir.usmp.enable"] = False

    with tvm.transform.PassContext(opt_level=3, config=config):
        if USE_CMSIS_NN:
            # When we are using CMSIS-NN, TVM searches for patterns in the
            # relay graph that it can offload to the CMSIS-NN kernels.
            relay_mod = cmsisnn.partition_for_cmsisnn(relay_mod, params, mcpu=TARGET.mcpu)
        lowered = tvm.relay.build(
            relay_mod, target=TARGET, params=params, runtime=RUNTIME, executor=EXECUTOR
        )
    parameter_size = len(tvm.runtime.save_param_dict(lowered.get_params()))
    print(f"Model parameter size: {parameter_size}")
    # --------------------------------------------

    # export -------------------------------------
    export_model_library_format(lowered, TAR_PATH)
    # --------------------------------------------

if __name__ == "__main__":
    microTVM()