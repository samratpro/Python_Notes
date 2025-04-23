### obfuscate
```
https://pyob.oxyry.com/
https://pyobfuscate.com/pyd
https://freecodingtools.org/tools/obfuscator/python
https://github.com/dashingsoft/pyarmor-webui
https://pyarmor.readthedocs.io/en/stable/tutorial/getting-started.html#obfuscating-one-script
https://www.python.org/downloads/windows/
https://jrsoftware.org/isdl.php#stable
https://drive.google.com/drive/folders/1NuUfle3LgGdWI6Z-GHdFJ4zJYkoVMQ8E?usp=sharing
```
file attacthed
```bash
pip install pyarmor
python convert_to_utf8.py
python replace_with_obfuscated.py
```
```bash
pip install cryptography
```

encrypt.py
```py
import os
from cryptography.fernet import Fernet

# 1️⃣ Generate a new encryption key (Run this only once and save it securely)
key = Fernet.generate_key()
cipher = Fernet(key)

print(f"🔑 Save this key securely: {key.decode()}")

# 2️⃣ Encrypt all Python files in the 'app' folder
source_folder = "app/"
for root, _, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".py"):  # Encrypt only .py files
            file_path = os.path.join(root, file)

            # Read and encrypt the file content
            with open(file_path, "rb") as f:
                encrypted_data = cipher.encrypt(f.read())

            # Save as .enc file
            with open(file_path.replace(".py", ".enc"), "wb") as f:
                f.write(encrypted_data)

            os.remove(file_path)  # Delete the original .py file

print("✅ All Python files encrypted!")

```
decryptor.py
```py
from cryptography.fernet import Fernet
import os

# 1️⃣ Store your encryption key (Replace with your actual key)
key = b"your-saved-key-here"  # Replace this with the key from encrypt.py
cipher = Fernet(key)

# 2️⃣ Decrypt & run the main script
main_enc_path = "app/main.enc"

if os.path.exists(main_enc_path):
    with open(main_enc_path, "rb") as f:
        encrypted_code = f.read()

    decrypted_code = cipher.decrypt(encrypted_code)
    exec(decrypted_code)  # Run the decrypted script in memory
else:
    print("❌ Error: Encrypted file not found!")
```

```
python -m compileall -b C:\Users\pc\Desktop\fish_dealer_software\venv\Lib\site-packages\
mkdir C:\Users\pc\Desktop\fish_dealer_software\external_libs
xcopy /E /I C:\Users\pc\Desktop\fish_dealer_software\venv\Lib\site-packages\__pycache__\* C:\Users\pc\Desktop\fish_dealer_software\external_libs\
```


### Embeded Python
```
https://www.python.org/downloads/windows/
https://www.python.org/downloads/source/
https://www.python.org/downloads/macos/
```
- Download unzip and keep embeded python in same project directory
- Example rename here `embeded_python`
- But for real uses only keep `python` folder for best practice
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
embeded_python\python -m pip uninstall -y -r requirements.txt
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
### runner.bat
```
@echo off
cd /d %~dp0
python\pythonw.exe app.py
# python\python.exe app.py
```
### run.vbs
```
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "runner.bat", 0, False
```
## Example Folder Structure
```
- features
- font
- forms
- icons
- images
- pages
- python
- static
- ui
app.py
dashboard.py
installer.iss
login.py
logo.ico
models.py
run.vbs
runner.bat
```
## Example installer.iss
```
; Define installer name and output directory
[Setup]
AppName=Fish Dealer Software
AppVersion=5.0
DefaultDirName={localappdata}\FishDealerSoftware_5
DefaultGroupName=Fish Dealer Software 5.0
OutputBaseFilename=FishDealerSetup_5
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\pc\Desktop\pyhton\fish_dealer_software\static\logo.ico

; Wizard images (if needed)
WizardImageFile=C:\Users\pc\Desktop\pyhton\fish_dealer_software\static\appbanner.bmp
WizardSmallImageFile=C:\Users\pc\Desktop\pyhton\fish_dealer_software\static\logo.bmp

; Silent installation option
DisableDirPage=no
DisableProgramGroupPage=yes

; Include Python interpreter and app files
[Files]
Source: "C:\Users\pc\Desktop\pyhton\fish_dealer_software\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish_dealer_software\python\*"; DestDir: "{app}\python"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish_dealer_software\font\*"; DestDir: "{app}\font"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish_dealer_software\icons\*"; DestDir: "{app}\icons"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish_dealer_software\images\*"; DestDir: "{app}\images"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish_dealer_software\run.vbs"; DestDir: "{app}"

; Create necessary folders
[Dirs]
Name: "{app}"; Permissions: everyone-full
Name: "{localappdata}\FishDealerSoftware"; Permissions: everyone-full

; Registry settings (optional)
[Registry]
Root: HKCU; Subkey: "Software\FishDealerSoftware2"; Flags: uninsdeletekey

; Shortcuts
[Icons]
Name: "{group}\Fish Dealer Software"; Filename: "{app}\run.vbs"; WorkingDir: "{app}"; IconFilename: "{app}\static\logo.ico"
Name: "{group}\Uninstall Fish Dealer Software"; Filename: "{uninstallexe}"; IconFilename: "{app}\static\logo.ico"
Name: "{commondesktop}\Fish Dealer Software"; Filename: "{app}\run.vbs"; WorkingDir: "{app}"; IconFilename: "{app}\static\logo.ico"; Tasks: desktopicon

; Run the application after installation
[Run]
Filename: "{app}\run.vbs"; Description: "{cm:LaunchProgram, Fish Dealer Software}"; Flags: nowait postinstall skipifsilent

; Uninstaller (removes everything)
[UninstallDelete]
Type: filesandordirs; Name: "{app}"
Type: filesandordirs; Name: "{localappdata}\FishDealerSoftware"

; Optional tasks
[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
```


