# Packaging For Windows
## 01. Pyinstaller Bootloader for C++ compiler
```
https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184
```
- Windows: (!https://visualstudio.microsoft.com/downloads/) Visual Studio Build Tools
           (Ensure you select MSVC, CMake, and Windows SDK during installation C, C++).
- Linux/macOS: Install gcc, clang, make, and zlib development headers.
```
# in any directory
git clone --recursive https://github.com/pyinstaller/pyinstaller.git
cd pyinstaller/bootloader
python ./waf all  # windows
python3 ./waf all  # Linux/macOS

# go back to the PyInstaller directory
pip install .
```
```
active local env
pip install --no-deps pyinstaller
pip install --no-deps auto-py-to-exe
pip install --no-deps --force-reinstall pyinstaller
pyinstaller --help | findstr "bootloader"
python -c "import PyInstaller; print(PyInstaller.__file__)"  
```

## 02. Generate Portable exe file
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

## 03. Packging
```
install inno setup software: https://jrsoftware.org/isdl.php
Open Software, and create a new "Script with setup Wizard" input one by one data
```
### Modify Some codes after setup Wizard
```
[Setup]
DefaultDirName={userappdata}\{#MyAppName}
# It will chanage install Dir " Program File (x86) " to "Appdata" folder, cause (x86) can't modify db file
DisableDirPage=no                           # For this also user can change dir while installing software

[Files]
Source: "C:\Users\pc\Desktop\project_dir\output\dbfile.db"; DestDir: "{commonappdata}\{#MyAppName}"; Flags: ignoreversion; Permissions: users-modify

for bulk icon add folder
Source: "C:\Users\pc\Desktop\project_dir\output\icons\*.svg"; DestDir: "{app}\icons"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\project_dir\output\images\*.png"; DestDir: "{app}\images"; Flags: ignoreversion
Defined that this file must be modified by user or software

```
## Modify Icon files
```
[Setup]
; Custom Wizard Image, must be .bmp and ico format
WizardImageFile=C:\Users\pc\Desktop\tkinter_practice\AIWritting App\output\banner.bmp
WizardSmallImageFile=C:\Users\pc\Desktop\tkinter_practice\AIWritting App\output\wizard_small_icon.bmp
SetupIconFile=C:\Users\pc\Desktop\tkinter_practice\AIWritting App\output\logo.ico


# Banner WizardImageFile = 202 X 386
# WizardSmallImageFile = 56 X 58

UninstallFilesDir=Uninstall\exe\{#MyAppNam}


```
## Example
```ini
#define MyAppName "Fish Dealer Software"
#define MyAppVersion "1.5"
#define MyAppPublisher "Osman Fish"
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "App.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
AppId={{77B47AEF-8BD1-4F85-9E7F-DEE89A05DFC1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userappdata}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
DisableDirPage=no
OutputBaseFilename=mysetup
WizardImageFile=C:\Users\pc\Desktop\fish_dealer_software\output\appbanner.bmp
WizardSmallImageFile=C:\Users\pc\Desktop\fish_dealer_software\output\logo.bmp
SetupIconFile=C:\Users\pc\Desktop\fish_dealer_software\output\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallFilesDir={app}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\logo.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\logo.bmp"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\appbanner.bmp"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\icons\*.svg"; DestDir: "{app}\icons"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\images\*.png"; DestDir: "{app}\images"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\font\*.ttf"; DestDir: "{app}\font"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\font\arial.ttf"; DestDir: "{app}\font"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\font\nato.ttf"; DestDir: "{app}\font"; Flags: ignoreversion

[Dirs]
Name: "{commonappdata}\{#MyAppName}"; Permissions: users-full

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\logo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\logo.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\business.db"
Type: files; Name: "{app}\logo.ico"
Type: files; Name: "{app}\logo.bmp"
Type: files; Name: "{app}\appbanner.bmp"
Type: files; Name: "{app}\icons\*.svg"
Type: files; Name: "{app}\images\*.png"
Type: files; Name: "{app}\font\*.ttf"
Type: files; Name: "{app}\font\arial.ttf"
Type: files; Name: "{app}\font\nato.ttf"
```
