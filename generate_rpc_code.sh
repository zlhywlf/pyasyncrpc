RPC_PATH='tests'
PROTO_PATH=$RPC_PATH/rpc

python3 -m grpc_tools.protoc \
-I$RPC_PATH \
--python_out=$RPC_PATH \
--pyi_out=$RPC_PATH \
--grpc_python_out=$RPC_PATH \
$PROTO_PATH/simple.proto
