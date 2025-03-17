package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.0.0"
	return C.CString(version)
}
