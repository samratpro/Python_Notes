### Embeded Python
```
https://www.python.org/downloads/windows/
https://www.python.org/downloads/source/
https://www.python.org/downloads/macos/
```
### Prepare pip 
Keep embeded python in same project directory
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



