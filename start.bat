@echo off
cd %-dp0
if not exist python (
	curl https://www.python.org/ftp/python/3.12.5/python-3.12.5-embed-amd64.zip > python.zip
	mkdir python
	powershell -command "Expand-Archive -Force python.zip python
	curl https://bootstrap.pypa.io/get-pip.py > python\get-pip.py
	cd %~dp0python
	python.exe get-pip.py
	copy python312._pth python312._pth.save
	cd %~dp0
)

del python\python312._pth
echo python312.zip > python\python312._pth
echo . >> python\python312._pth
echo %~dp0python\ >> python\python312._pth
echo %~dp0python\DLLs >> python\python312._pth
echo %~dp0python\lib >> python\python312._pth
echo %~dp0python\lib\plat-win >> python\python312._pth
echo %~dp0python\lib\site-packages >> python\python312._pth

python\python -m site
python\python -m pip install virtualenv
python\python -m virtualenv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
python main.py