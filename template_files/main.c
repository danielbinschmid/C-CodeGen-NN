#include "tvmgen_default.h"

// input and output data header
#include "input.h"
#include "output.h"
#include <stdio.h>
#include <stdlib.h>
#define MAX 100
// #define LOGGING 1

int main(int argc, char** argv) {
#ifdef LOGGING
    printf("Starting simulation.\n");
#endif
    struct tvmgen_default_inputs inputs = {
        .in = input,
    };

    void* output_buffer = malloc(output_len * sizeof(float)+1);
    if (output_buffer == NULL) return -1;
    struct tvmgen_default_outputs outputs = {
        .output = output_buffer,
    };

    tvmgen_default_run(
        &inputs,
        &outputs
    );
#ifdef LOGGING
    float* inp_ = (float*) input;
    for (size_t i = 0; i < input_len; i++) {
        char buf[MAX];
        gcvt(inp_[i], 6, buf);

        printf("INFO (input): ");
        printf(buf);
        printf("\n");

    }

    float* out_hat = (float*) outputs.output;
    float* out_gold = (float*) output;
    for(size_t i = 0; i < output_len; i++) {
        char out_hat_str[MAX];
        gcvt(out_hat[i], 6, out_hat_str);

        char out_gold_str[MAX];
        gcvt(out_gold[i], 6, out_gold_str);

        printf("COMP (out_hat, out_gold): (");
        printf(out_hat_str);
        printf(", ");
        printf(out_gold_str);
        printf(")\n");
    }
    printf("Done.\n");
#endif
    
    free(output_buffer);
    
}