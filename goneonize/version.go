package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "2.0.0.2"
	return C.CString(version)
}
