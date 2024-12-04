git clone --depth 1 https://github.com/tulir/whatsmeow.git
rm -rf goneonize/defproto
mv whatsmeow/proto goneonize/defproto
rm goneonize/defproto/*/*.pb.*
rm goneonize/defproto/*/*.go
rm goneonize/defproto/.gitignore
rm goneonize/defproto/*.*
rm -rf whatsmeow
cp goneonize/Neonize.proto goneonize/defproto