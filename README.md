# C-CodeGenNN

This repository contains a toolchain to generate code for neural networks described by the ONNX format to *dependency free* C code using ApacheTVM. <br>
The target is to generate C code that can be used for circuit simulation frameworks such as Chipyard or Synopsis.

## Features

- FrontEnds: ONNX
- Build tools: standard _gcc_, _riscv64-unknown-elf_, _riscv64-unknown-elf baremetal_

## Setup

- Tested with python version 3.9.15
- Dependency management via poetry

After activating fresh virtual python environment:
```s
$ pip install --upgrade pip
$ pip install poetry
$ poetry install
```
