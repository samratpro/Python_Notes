# Packaging For Windows
```
https://www.python.org/downloads/windows/
https://jrsoftware.org/isdl.php#stable
https://drive.google.com/drive/folders/1NuUfle3LgGdWI6Z-GHdFJ4zJYkoVMQ8E?usp=sharing
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

# Bat method 
run.bat
```
@echo off
%~dp0venv\Scripts\python.exe %~dp0main.py
```
```
@echo off
%~dp0venv\Scripts\pythonw.exe %~dp0main.py
```

# Example innosetup iss file 
```
; Define installer name and output directory
[Setup]
AppName=Fish Dealer Software 2
AppVersion=1.0
DefaultDirName={localappdata}\FishDealerSoftware2
DefaultGroupName=Fish Dealer Software 2
OutputBaseFilename=FishDealerSetup2
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\pc\Desktop\pyhton\fish\static\logo.ico

; Wizard images (if needed)
WizardImageFile=C:\Users\pc\Desktop\pyhton\fish\static\appbanner.bmp
WizardSmallImageFile=C:\Users\pc\Desktop\pyhton\fish\static\logo.bmp

; Silent installation option
DisableDirPage=no
DisableProgramGroupPage=yes

; Include Python interpreter and app files
[Files]
Source: "C:\Users\pc\Desktop\pyhton\fish\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish\venv\*"; DestDir: "{app}\venv"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish\font\*"; DestDir: "{app}\font"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish\icons\*"; DestDir: "{app}\icons"; Flags: recursesubdirs
Source: "C:\Users\pc\Desktop\pyhton\fish\images\*"; DestDir: "{app}\images"; Flags: recursesubdirs

; Create necessary folders
[Dirs]
Name: "{app}"; Permissions: everyone-full
Name: "{localappdata}\FishDealerSoftware2"; Permissions: everyone-full

; Registry settings (optional)
[Registry]
Root: HKCU; Subkey: "Software\FishDealerSoftware2"; Flags: uninsdeletekey

; Shortcuts
[Icons]
Name: "{group}\Fish Dealer Software 2"; Filename: "{app}\venv\Scripts\pythonw.exe"; Parameters: """{app}\main.py"""; WorkingDir: "{app}"; IconFilename: "{app}\static\logo.ico"
Name: "{group}\Uninstall Fish Dealer Software 2"; Filename: "{uninstallexe}"; IconFilename: "{app}\static\logo.ico"
Name: "{commondesktop}\Fish Dealer Software 2"; Filename: "{app}\venv\Scripts\pythonw.exe"; Parameters: """{app}\main.py"""; WorkingDir: "{app}"; IconFilename: "{app}\static\logo.ico"; Tasks: desktopicon

; Run the application after installation
[Run]
Filename: "{app}\venv\Scripts\pythonw.exe"; Parameters: """{app}\main.py"""; WorkingDir: "{app}"; Flags: nowait postinstall

; Uninstaller (removes everything)
[UninstallDelete]
Type: filesandordirs; Name: "{app}"
Type: filesandordirs; Name: "{localappdata}\FishDealerSoftware2"

; Optional tasks
[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
```
