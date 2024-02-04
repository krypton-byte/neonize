typedef void (*ptr_to_python_function)(bool);
typedef void (*ptr_to_python_function_string) (char*);
typedef void (*ptr_to_python_function_bytes)(const char*, size_t);
typedef void (*ptr_to_python_function_callback_bytes)(const char*, size_t, int);

static inline void call_c_func(ptr_to_python_function ptr, bool stat) {
	(ptr)(stat);
}
static inline void call_c_func_string(ptr_to_python_function_string ptr, char* xStr) {
	(ptr)(xStr);
}

static inline void call_c_func_bytes(ptr_to_python_function_bytes ptr, const char* data, size_t size) {
	(ptr)(data, size);
}

static inline void call_c_func_callback_bytes(ptr_to_python_function_callback_bytes ptr, const char* data, size_t size, int code) {
	(ptr)(data, size, code);
}