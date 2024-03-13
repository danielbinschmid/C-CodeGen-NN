import onnxruntime as ort
import numpy as np
import argparse

def generate_io_from_onnx(onnx_file_path, input_npy_path, output_npy_path):
    # Load the ONNX model
    session = ort.InferenceSession(onnx_file_path)

    # Assuming the model has only one input and one output
    input_name = session.get_inputs()[0].name
    input_shape = session.get_inputs()[0].shape
    input_type = session.get_inputs()[0].type

    # Generate dummy input data
    if input_type == 'tensor(float)':
        dummy_input = np.random.randn(*input_shape).astype(np.float32)
    elif input_type == 'tensor(int64)':
        dummy_input = np.random.randint(0, 100, size=input_shape).astype(np.int64)
    else:
        raise ValueError("Unsupported input type")

    # Run inference
    outputs = session.run(None, {input_name: dummy_input})

    # Save input and output as .npy files
    np.save(input_npy_path, dummy_input)
    np.save(output_npy_path, outputs[0])  # Assuming only one output

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate input and output NumPy files from a ONNX model")
    parser.add_argument("--onnx_path", required=True, help="Path to the ONNX model file")
    parser.add_argument("--input_npy_path", required=True, help="Path to save the generated input .npy file")
    parser.add_argument("--output_npy_path", required=True, help="Path to save the generated output .npy file")

    args = parser.parse_args()

    generate_io_from_onnx(args.onnx_path, args.input_npy_path, args.output_npy_path)
