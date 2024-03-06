package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "8.0.0"
	return C.CString(version)
}
