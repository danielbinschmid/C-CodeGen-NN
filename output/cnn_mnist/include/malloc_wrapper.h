#include <stdint.h>
#include <stdlib.h>

/**
 * Wrapper for TVMBackendAllocWorkspace of TVM runtime. Calls malloc.
*/
void*  TVMBackendAllocWorkspace(int arg0, int arg1, uint64_t size, int arg3, int arg4) {
    return malloc(size);
}

/**
 * Wrapper for TVMBackendAllocWorkspace of TVM runtime. Calls free.
*/
int TVMBackendFreeWorkspace(int arg0, int arg1, void* ptr) {
    free(ptr);
    return 0;
}