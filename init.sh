pip3 install -e . -i https://mirrors.aliyun.com/pypi/simple
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
pre-commit install --install-hooks
bash ./generate_rpc_code.sh
