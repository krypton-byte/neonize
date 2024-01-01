GOOS=linux GOARCH=amd64 CGO_ENABLED=1 go build -buildmode=c-shared -ldflags=-s -o gocode.so main.go
protoc --go_out=. Neonize.proto && protoc --python_out=. --mypy_out=. Neonize.proto
protoc --go_out=. Neonize.proto && protoc --python_out=../proto --mypy_out=../proto Neonize.proto
protoc --go_out=. Neonize.proto && protoc --python_out=../proto --mypy_out=../proto def.proto



