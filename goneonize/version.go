package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.1.0"
	return C.CString(version)
}
