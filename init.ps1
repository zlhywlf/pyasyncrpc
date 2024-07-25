pip install -e . -i https://mirrors.aliyun.com/pypi/simple;
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple;
pre-commit install --install-hooks;
.\generate_rpc_code.ps1
