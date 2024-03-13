#!/bin/bash

# arguments
ONNX_FILE_PATH="./model_files/onnx/mnist/mnist-12.onnx"
MODEL_NAME="cnn_mnist"

# create temporary directory
if [ -d "./tmp" ]; then
  rm -r "./tmp"
fi
mkdir tmp

# generate mlf .tar file with apache tvm
OUT_TAR="./tmp/"$MODEL_NAME"_mlf.tar"
python ./runnables/generate_mlf_from_onnx.py -onnx_model $ONNX_FILE_PATH -out_tar $OUT_TAR

# untar
UNTAR_DIR="./tmp/"$MODEL_NAME
mkdir $UNTAR_DIR
tar -xf $OUT_TAR -C $UNTAR_DIR

# transform generated code

