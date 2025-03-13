### obfuscate
```
https://pyob.oxyry.com/
https://pyobfuscate.com/pyd
https://freecodingtools.org/tools/obfuscator/python
https://github.com/dashingsoft/pyarmor-webui
https://pyarmor.readthedocs.io/en/stable/tutorial/getting-started.html#obfuscating-one-script
```
file attacthed
```bash
pip install pyarmor
python convert_to_utf8.py
python replace_with_obfuscated.py
```

### Embeded Python
```
https://www.python.org/downloads/windows/
https://www.python.org/downloads/source/
https://www.python.org/downloads/macos/
```
- Download unzip and keep embeded python in same project directory
- Example rename here `embeded_python`
### Prepare pip 
```cmd
curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
embeded_python\python get-pip.py
```
### python39._pth
embeded_python\python39._pth
```
python39.zip
.
Lib\site-packages
```
### Manage Pip
```
embeded_python\python -m pip list
embeded_python\python -m pip freeze
embeded_python\python -m pip install "module name"
embeded_python\python -m pip freeze > requirements.txt
embeded_python\python -m pip install -r requirements.txt
```
### Startup file, main.py or app.py
add this on header
```py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```
### Run
```
embeded_python\python app.py
```
### run.bat
```
@echo off
%~dp0embeded_python\pythonw.exe %~dp0 app.py
pause
endlocal
```



