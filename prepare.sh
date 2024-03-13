#!/bin/bash

python ./runnables/gen_rndn_verification_data.py \
    --onnx_path "./model_files/onnx/mnist/mnist-12.onnx" \
    --input_npy_path "inp.npy" \
    --output_npy_path "outp.npy"
