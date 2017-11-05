SET PYTHON_PATH=C:\Users\Timothy\AppData\Local\Programs\Python\Python35-32\python.exe
SET APP_DIR=C:\Repos\event_loop
cd %APP_DIR%


:: %PYTHON_PATH% demo.py --help
:: %PYTHON_PATH% demo.py --version
%PYTHON_PATH% demo.py --loops 5 --powers 4 --runtime 18 --display True
