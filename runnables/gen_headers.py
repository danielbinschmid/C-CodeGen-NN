import os
import pathlib
import numpy as np
from typing import List
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-data_folder', help='folder containing verification data, i.e. the inp.npy and outp.npy file(s)')
parser.add_argument('-n_inputs', help='number of inputs')
parser.add_argument('-n_outputs', help='numnber of outputs')
parser.add_argument('-out_folder', help='the target folder in which the headers shall be placed')
args = parser.parse_args()


OUTPUT_PATH     = args.out_folder
INPUT_BASE_PATH = args.data_folder
N_INPUTS 	= int(args.n_inputs)
N_OUTPUTS 	= int(args.n_outputs)

def create_header_file(name: str, section: str, tensor_name: str, tensor_data: np.ndarray, output_path: str):
    """
    This function generates a header file containing the data from the numpy array provided.
    """
    file_path = pathlib.Path(f"{output_path}/" + name).resolve()
    # Create header file with npy_data as a C array
    raw_path = file_path.with_suffix(".h").resolve()
    with open(raw_path, "w") as header_file:
        header_file.write(
            "#include <tvmgen_default.h>\n"
            + "#include <stddef.h>\n"
            + f"const size_t {tensor_name}_len = {tensor_data.size};\n"
            + f'uint8_t {tensor_name}[] __attribute__((section("{section}"), aligned(16))) = "'
        )
        data_hexstr = tensor_data.tobytes().hex()
        for i in range(0, len(data_hexstr), 2):
            header_file.write(f"\\x{data_hexstr[i:i+2]}")
        header_file.write('";\n\n')

def create_headers_multiple_inputs_multiple_outputs():
    CREATE_HEADERS_FLAG = True

    # load data
    if N_INPUTS > 1:
        INP_DATA_PATHS = [os.path.join(INPUT_BASE_PATH, "inp" + str(i + 1) + ".npy") for i in range(N_INPUTS)]
    else:
        INP_DATA_PATHS = [os.path.join(INPUT_BASE_PATH, "inp.npy")]

    if N_OUTPUTS > 1:
        OUTP_DATA_PATHS = [os.path.join(INPUT_BASE_PATH, "outp" + str(i + 1) + ".npy") for i in range(N_OUTPUTS)]
    else:
        OUTP_DATA_PATHS = [os.path.join(INPUT_BASE_PATH, "outp.npy")]

    inps_data: List[np.ndarray] = [np.load(inp_data_path) for inp_data_path in INP_DATA_PATHS]
    outps_data: List[np.ndarray] = [np.load(outp_data_path) for outp_data_path in OUTP_DATA_PATHS]

    # input
    if CREATE_HEADERS_FLAG:
        if N_INPUTS > 1:
            for i in range(N_INPUTS):
                create_header_file(
                name="input" + str(i + 1) +  ".h",
                section="input_data_sec" + str(i + 1),
                tensor_name="input" + str(i + 1),
                tensor_data=inps_data[i],
                output_path=OUTPUT_PATH
            )    
        else:
            create_header_file(
                name="input.h",
                section="input_data_sec",
                tensor_name="input",
                tensor_data=inps_data[0],
                output_path=OUTPUT_PATH
            )

    # output
    if CREATE_HEADERS_FLAG:
        if N_OUTPUTS > 1:
            for i in range(N_OUTPUTS):
                create_header_file(
                name="output" + str(i + 1) +  ".h",
                section="output_data_sec" + str(i + 1),
                tensor_name="output" + str(i + 1),
                tensor_data=inps_data[i],
                output_path=OUTPUT_PATH
            )  
        else:
            create_header_file(
                name="output.h",
                section="output_data_sec",
                tensor_name="output",
                tensor_data=outps_data[0],
                output_path=OUTPUT_PATH
            )

create_headers_multiple_inputs_multiple_outputs()
