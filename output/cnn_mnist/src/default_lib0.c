#define TVM_DLL __attribute__((visibility("default")))
#ifdef __cplusplus
extern "C" {
#endif
#include <tvmgen_default.h>
TVM_DLL int32_t tvmgen_default___tvm_main__(void* Input3,void* output0);
int32_t tvmgen_default_run(struct tvmgen_default_inputs* inputs,struct tvmgen_default_outputs* outputs) {return tvmgen_default___tvm_main__(inputs->Input3,outputs->output);
}
#ifdef __cplusplus
}
#endif
;