:: Set environment variables
set GOOS=windows
set GOARCH=amd64
set CGO_ENABLED=1
set CC=x86_64-w64-mingw32-gcc

:: Generate Go code using protoc
protoc --go_out=. Neonize.proto def.proto
protoc --python_out=../proto --mypy_out=../proto def.proto Neonize.proto

:: Run Python build script
python build.py

:: Generate Go code for gRPC
protoc --go_out=. --go-grpc_out=. -I . Neonize.proto def.proto

:: Clean up and move generated files
if exist defproto rmdir /s /q defproto
if exist github.com/krypton-byte/neonize/defproto move github.com/krypton-byte/neonize/defproto defproto
rmdir /s /q github.com

:: Build the Go shared library
go build -buildmode=c-shared -ldflags=-s -o neonize.dll main.go
move /Y neonize.dll ..
