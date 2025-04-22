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


