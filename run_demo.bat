SET PYTHON_PATH=C:\Users\Timothy\AppData\Local\Programs\Python\Python35-32\python.exe
SET APP_DIR=C:\Repos\event_loop
cd %APP_DIR%

:: HOW TO GET HELP AND VERSION NUMBER
:: %PYTHON_PATH% demo.py --help
:: %PYTHON_PATH% demo.py --version

:: CHOOSE THE DEMO YOU WANT TO RUN. THEY ARE PRE-CONFIGURED TO BE DECENT DEMOS.
:: %PYTHON_PATH% demo.py --tasks 500 --powers 5 --runtime 130 --demo work
%PYTHON_PATH% demo.py --tasks 3 --runtime 20 --demo quest
