SET PYTHON_PATH=C:\Users\Timothy\AppData\Local\Programs\Python\Python35-32\python.exe
SET APP_DIR=C:\Repos\event_loop
cd %APP_DIR%

:: HOW TO GET HELP AND VERSION NUMBER
:: %PYTHON_PATH% demo.py --version
:: %PYTHON_PATH% demo.py --help

:: WORK DEMO - ie: 'MINING'
%PYTHON_PATH% demo.py --cycles 10 --demo work

:: QUEST DEMO
%PYTHON_PATH% demo.py --cycles 3 --demo quest
