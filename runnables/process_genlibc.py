import argparse

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    with open(output_file_path, 'w') as file:
        for line in lines:
            if '#include "tvm/runtime/c_runtime_api.h"' in line:
                file.write('#define TVM_DLL __attribute__((visibility("default")))\n')
            elif '#include "tvm/runtime/c_backend_api.h"' in line:
                file.write('#include <stddef.h>\n#include <stdint.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <stdbool.h>\n#include "malloc_wrapper.h"\n')
            else:
                file.write(line)

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Process generated lib files from MLF format of Apache TVM.")

    # Add the arguments
    parser.add_argument('--input', '-i', required=True, help="Input file path")
    parser.add_argument('--output', '-o', required=True, help="Output file path")

    # Parse the arguments
    args = parser.parse_args()

    # Process the file
    process_file(args.input, args.output)
