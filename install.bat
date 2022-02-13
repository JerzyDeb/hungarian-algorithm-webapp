@ECHO OFF
setlocal
mkdir c:\hungarian_algorithm_webapp
.\python\python.exe -m virtualenv c:\hungarian_algorithm_webapp\venv
copy .\python\python39.zip  c:\hungarian_algorithm_webapp\venv\Scripts\
call c:\hungarian_algorithm_webapp\venv\Scripts\activate.bat
c:\hungarian_algorithm_webapp\venv\Scripts\pip.exe install -r .\d_app\requirements.txt
c:\hungarian_algorithm_webapp\venv\Scripts\python.exe .\d_app\manage.py collectstatic
c:\hungarian_algorithm_webapp\venv\Scripts\python.exe .\d_app\manage.py migrate
PAUSE