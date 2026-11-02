package main

import "C"

//export GetVersion
func GetVersion() *C.char {
	version := "0.8.0"
	return C.CString(version)
}
