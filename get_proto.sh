git clone --depth 1 https://github.com/tulir/whatsmeow.git
rm -rf goneonize/proto/waproto
mv whatsmeow/proto goneonize/waproto
rm goneonize/waproto/proto/*/*.pb.*
rm -rf whatsmeow