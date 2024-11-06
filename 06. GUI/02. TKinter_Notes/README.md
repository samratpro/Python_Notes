# Packaging For Windows
```
https://customtkinter.tomschimansky.com/documentation/
```
## Pyinstaller Bootloader for C++ compiler
```
https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184

1. Uninstall Existing pyinstaller
2. Install Microsoft Visual C++ Compiler
3. Run Compiler
4. Download Update git repo: http://github.com/pyinstaller/pyinstaller/releases
5. F:\DriverName\pyinstaller-5.13.0\pyinstaller-5.13.0\bootloader
   from here run, " python.exe ./waf all "
   check the " waf " file in this folder before run the above command
6. F:\DriverName\pyinstaller-5.13.0\pyinstaller-5.13.0
   come back and from this folder run " pip install . " or  " python setup.py install "
7. Bootloader has been completed
   
```

## Generate Portable exe file
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

## Packging
```
install inno setup software: https://jrsoftware.org/isdl.php
Open Software, and create a new "Script with setup Wizard" input one by one data
```
### Modify Some codes after setup Wizard
```
[Setup]
DefaultDirName={userappdata}\{#MyAppName}   # Chanage install Dir " Program File (x86) " to "Appdata" folder
DisableDirPage=no                           # For this also user can change dir while installing software

" Program File (x86) " can't modify the database

[Files]
Source: "C:\Users\pc\Desktop\tkinter_practice\AIWritting App\output\postdb.db"; DestDir: "{commonappdata}\{#MyAppName}"; Flags: ignoreversion; Permissions: users-modify

Defined that this file must be modified by user or software

```
## Modify
```
[Setup]
; Custom Wizard Image, must be .bmp and ico format
WizardImageFile=C:\Users\pc\Desktop\tkinter_practice\AIWritting App\output\banner.bmp
WizardSmallImageFile=C:\Users\pc\Desktop\tkinter_practice\AIWritting App\output\wizard_small_icon.bmp
SetupIconFile=C:\Users\pc\Desktop\tkinter_practice\AIWritting App\output\logo.ico


# Banner WizardImageFile = 202 X 386
# WizardSmallImageFile = 56 X 58

UninstallFilesDir=Uninstall\exe\{#NAME_OF_APP}


```
### Run 
```
Now simply run for packing software
```
