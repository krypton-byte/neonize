#ifndef PYTHONPTR_H
#define PYTHONPTR_H
// example.h
#include <stddef.h>
typedef void (*ptr_to_python_function)(bool);
// Tipe data pointer ke fungsi C yang menerima string
typedef void (*ptr_to_python_function_string)(char*);

// Tipe data pointer ke fungsi C yang menerima data bytes dan ukurannya
typedef void (*ptr_to_python_function_bytes)(const char*, size_t);

typedef void (*ptr_to_python_function_callback_bytes)(const char*, size_t, int);
static inline void call_c_func(ptr_to_python_function ptr, bool stat) {
    (ptr)(stat);
}
// Deklarasi fungsi untuk memanggil fungsi C yang menerima string
static inline void call_c_func_string(ptr_to_python_function_string ptr, char* xStr) {
    (ptr)(xStr);
}
// Deklarasi fungsi untuk memanggil fungsi C yang menerima data bytes dan ukurannya
static inline void call_c_func_bytes(ptr_to_python_function_bytes ptr, const char* data, size_t size) {
    (ptr)(data, size);
}
static inline void call_c_func_callback_bytes(ptr_to_python_function_callback_bytes ptr, const char* data, size_t size, int code){
    (ptr)(data, size, code);
}


#endif