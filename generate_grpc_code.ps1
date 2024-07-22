$Env:RPC_PATH = 'tests';

python -m grpc_tools.protoc `
-I $Env:RPC_PATH `
--python_out=$Env:RPC_PATH `
--pyi_out=$Env:RPC_PATH `
--grpc_python_out=$Env:RPC_PATH `
$Env:RPC_PATH/rpc/simple.proto;
