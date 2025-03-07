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
python -m compileall -b venv/Lib/site-packages/
mkdir external_libs
cp -r venv/Lib/site-packages/__pycache__/* external_libs/
```

Example innosetup iss file
```
[Setup]
AppName=My Secure PyQt6 App
AppVersion=1.0
DefaultDirName={pf}\MySecureApp
OutputBaseFilename=MySecureApp_Installer
Compression=lzma
SolidCompression=yes
WizardImageFile=C:\Users\pc\Desktop\fish_dealer_software\app\static\appbanner.bmp
WizardSmallImageFile=C:\Users\pc\Desktop\fish_dealer_software\app\static\logo.bmp
SetupIconFile=C:\Users\pc\Desktop\fish_dealer_software\app\static\logo.ico

[Files]
Source: "C:\Users\pc\Desktop\fish_dealer_software\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
Source: "C:\Users\pc\Desktop\fish_dealer_software\python\*"; DestDir: "{app}\python"; Flags: recursesubdirs createallsubdirs
Source: "C:\Users\pc\Desktop\fish_dealer_software\external_libs\*"; DestDir: "{app}\external_libs"; Flags: recursesubdirs createallsubdirs
Source: "C:\Users\pc\Desktop\fish_dealer_software\app\font\*"; DestDir: "{app}\fonts"; Flags: recursesubdirs createallsubdirs
Source: "C:\Users\pc\Desktop\fish_dealer_software\app\font\*"; DestDir: "{app}\icons"; Flags: recursesubdirs createallsubdirs
Source: "C:\Users\pc\Desktop\fish_dealer_software\app\images\*"; DestDir: "{app}\images"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MySecureApp"; Filename: "{app}\run.bat"; WorkingDir: "{app}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Registry]
Root: HKCU; Subkey: "Software\MySecureApp"; ValueType: string; ValueName: "InstallationDir"; ValueData: "{app}"

[Run]
Filename: "{app}\python\pythonw.exe"; Parameters: "{app}\decryptor.py"; WorkingDir: "{app}"; Description: "Launch My Secure App"; Flags: nowait postinstall skipifsilent
```
