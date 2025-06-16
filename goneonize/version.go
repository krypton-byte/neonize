package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.3.9.1"
	return C.CString(version)
}
