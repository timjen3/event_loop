SET PYTHON_PATH=C:\Users\Timothy\AppData\Local\Programs\Python\Python35-32\python.exe
SET APP_DIR=C:\Users\Timothy\PycharmProjects\CountersV2
cd %APP_DIR%


echo 'running demo'
:: %PYTHON_PATH% demo.py --help
:: %PYTHON_PATH% demo.py --version
%PYTHON_PATH% demo.py --loops 1 --powers 10 --plot True
echo 'demo complete'
