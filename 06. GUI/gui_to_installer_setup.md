# Packaging For Windows
```
https://www.python.org/downloads/windows/
https://jrsoftware.org/isdl.php#stable
https://drive.google.com/drive/folders/1NuUfle3LgGdWI6Z-GHdFJ4zJYkoVMQ8E?usp=sharing
https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
https://www.briggsoft.com/signgui.htm
```

## 01. Generate Portable exe file
### Install Packages
```
pip install pyinstaller
pip install auto-py-to-exe
```
### Input command in CMD or Git Bash
```
auto-py-to-exe
```
### Configure paths
```
1. Select the main script path
2. Select Onefile
3. Select Window Base
4. Select the Icon file (logo.ico)
5. Select additional files
6. Select Package Folder for Customtkinter or if required
to see the path and make this command:
pip show customtkinter
example path is:  C:\Users\pc\AppData\Local\Programs\Python\Python311\Lib\site-packages
```
### Generate exe
```
After completing all click on generate .PY To Exe button, also we can modify the output folder from setting
```
## Generate Certificate
```
New-SelfSignedCertificate -Type Custom -Subject "CN=Sofmake, O=Sofmake, C=US" -KeyUsage DigitalSignature -FriendlyName "My Friendly Cert Name" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

Get-ChildItem -Path Cert:\CurrentUser\My  # to see 

$thumb = "F2D86ADFA91BEEBF4EAF870B406DF5D7F373075E"
$cert = Get-Item "Cert:\CurrentUser\My\$thumb"
Export-PfxCertificate -Cert $cert -FilePath "C:\Users\pc\Desktop\fish_dealer_software\output\MyCertbing.pfx" -Password (Read-Host -AsSecureString "Enter password")
```
## Apply Certificate
```
- open signgui
- C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe (Eample : SingTool location)
- C:\Users\pc\Desktop\fish_dealer_software\output\MyCertbing.pfx (PFX file, password : given password to generate file)
- C:\Users\pc\Desktop\fish_dealer_software\output\app.exe (Output)
- SHA 256 (Signurate)
```

## 03. Packging
```
install inno setup software: https://jrsoftware.org/isdl.php
Open Software, and create a new "Script with setup Wizard" input one by one data
```
