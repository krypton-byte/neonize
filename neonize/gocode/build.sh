protoc --go_out=. Neonize.proto def.proto && protoc --python_out=../proto --mypy_out=../proto def.proto Neonize.proto
python3 build.py
protoc --go_out=. --go-grpc_out=. -I . Neonize.proto def.proto 
if [[ -f defproto ]]
then
rm -rf defproto
fi
mv -f github.com/krypton-byte/neonize/defproto/* defproto
rm -rf github.com/
GOOS=linux GOARCH=amd64 CGO_ENABLED=1 go build -buildmode=c-shared -ldflags=-s -o gocode.so main.go



