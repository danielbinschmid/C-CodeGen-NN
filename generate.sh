#!/bin/bash

# Usage: ./generate.sh

root_dir=$(pwd)

# configuration
IO_NP_FOLDER="$root_dir/model_files/onnx/mnist"
ONNX_FILE_PATH="$IO_NP_FOLDER/mnist-12.onnx"
MODEL_NAME="cnn_mnist"
N_INPUTS=1
N_OUTPUTS=1
MAKEFILE=$root_dir"/template_files/Makefile_Default-GCC"
MAIN_FILE=$root_dir"/template_files/main.c" # NOTE: only for single input and output
BAREMETAL=false

# constants
SPEC_FILE=$root_dir"/template_files/htif_nano.specs"
MALLOC_WRAPPER=$root_dir"/template_files/malloc_wrapper.h"

# create temporary directory
if [ -d "./tmp" ]; then
  rm -r "./tmp"
fi
mkdir tmp

# generate mlf .tar file with apache tvm
OUT_TAR="./tmp/"$MODEL_NAME"_mlf.tar"
python $root_dir/runnables/generate_mlf_from_onnx.py -onnx_model $ONNX_FILE_PATH -out_tar $OUT_TAR

# untar
UNTAR_DIR=$root_dir"/tmp/out_"$MODEL_NAME
mkdir $UNTAR_DIR
tar -xf $OUT_TAR -C $UNTAR_DIR

# process codegen output ----------------
cd $UNTAR_DIR

# move metadata to a metadata folder
mkdir generated_metadata
mv src ./generated_metadata
mv parameters ./generated_metadata
mv metadata.json ./generated_metadata

# top-level include and src dir
mkdir include
mkdir src
mv codegen/host/include/* include/
mv codegen/host/src/* src/

# cleanup
rm -r codegen
rm -r runtime # remove tvm runtime because of file size

# Add template. Generate headers; Add main.c file; Add Makefile; 
cp $MAKEFILE ./Makefile
cp $MALLOC_WRAPPER ./include
cp $MAIN_FILE ./src/main.c
if [ "$BAREMETAL" = true ]; then
  cp $SPEC_FILE ./
fi

# replace includes in generated C files
python $root_dir/runnables/process_genlibc.py -i ./src/default_lib0.c -o ./src/default_lib0.c
python $root_dir/runnables/process_genlibc.py -i ./src/default_lib1.c -o ./src/default_lib1.c

# --------------------------------------

# input and output data as C headers
python $root_dir/runnables/gen_headers.py -data_folder $IO_NP_FOLDER -out_folder ./include -n_inputs $N_INPUTS -n_outputs $N_INPUTS

# move output to project root
out_dir=$root_dir/out_$MODEL_NAME
if [ -d $out_dir ]; then
  rm -r $out_dir
fi
mv $UNTAR_DIR $root_dir
rm -r $root_dir/tmp
