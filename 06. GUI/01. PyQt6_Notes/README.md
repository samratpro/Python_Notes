# PyQt6 Components
This Repository is for noting the PyQt6 component after practice
```
my_project/
├── main.py
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── logger.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_model.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_view.py
│   │   ├── settings_view.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── main_controller.py
│   │   ├── settings_controller.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_service.py
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── custom_button.py
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── images/
│   │   ├── styles/
│   │   │   ├── main.qss
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helper.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_user_model.py
└── README.md
```
## START
```bash
pip install pyqt6
pip install pyqt6-tools
pip install pyqt-tools
```
```py
https://build-system.fman.io/qt-designer-download
https://feathericons.com/
https://drive.google.com/file/d/13wMzZ5AZ6H-8JFYmxiEr6FDa0_9sE9L6/view?usp=sharing
```
linux
```bash
sudo apt-get install pyqt5-dev-tools
sudo apt-get install pyqt6-dev-tools
```
#### Qt Designer Path
```bash
env\Lib\site-packages\qt6_applications\Qt\bin
```
#### UI to Py
Activate virtual Environment, if project in local environment: 
```bash
source env/scripts/activate
pyuic6 -x gui_path.ui -o py_path.py
```

#### Load UI file
```py
from PyQt6 import uic
uic.loadUi('hello.ui', window) # Functional
uic.loadUi('hello.ui',self) # Class base
```

#### Functional Way
```py
from PyQt6.QtWidgets import *
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.statusBar().showMessage("Welcome to here")
window.menuBar().addMenu("Open File")

window.setGeometry(0, 0, 700, 300)
window.show()
sys.exit(app.exec())
```

#### Class Base
```py
from PyQt6.QtWidgets import *
import sys
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 400)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
```
