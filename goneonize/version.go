package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.10.0"
	return C.CString(version)
}
