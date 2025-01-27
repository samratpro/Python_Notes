# Packaging For Windows
## 01. Pyinstaller Bootloader for C++ compiler
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
; Define application details
#define MyAppName "Fish Dealer Software" ; Change to your application name
#define MyAppVersion "1.5" ; Change to your application version
#define MyAppPublisher "Osman Fish" ; Change to your publisher name
#define MyAppURL "https://www.example.com/" ; Change to your application URL
#define MyAppExeName "App.exe" ; Change to your main executable file name
#define MyAppAssocName MyAppName + " File" ; Change if you want a different file association name
#define MyAppAssocExt ".myp" ; Change to your desired file extension
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt ; No need to change

[Setup]
AppId={{77B47AEF-8BD1-4F85-9E7F-DEE89A05DFC1} ; Generate a new GUID for your application
AppName={#MyAppName} ; No need to change
AppVersion={#MyAppVersion} ; No need to change
AppPublisher={#MyAppPublisher} ; No need to change
AppPublisherURL={#MyAppURL} ; No need to change
AppSupportURL={#MyAppURL} ; No need to change
AppUpdatesURL={#MyAppURL} ; No need to change
DefaultDirName={userappdata}\{#MyAppName} ; Change if you want a different installation directory
ChangesAssociations=yes ; Set to "no" if you don't want file associations
DisableProgramGroupPage=yes ; Set to "no" if you want a program group in the Start menu
DisableDirPage=no ; Set to "yes" if you want to hide the directory selection page
OutputBaseFilename=mysetup ; Change to your desired setup file name
SetupIconFile=C:\Users\pc\Desktop\fish_dealer_software\logo.ico ; Change to the path of your icon file
WizardSmallImageFile=C:\Users\pc\Desktop\fish_dealer_software\logo.bmp ; Change to the path of your wizard image
Compression=lzma ; No need to change
SolidCompression=yes ; No need to change
WizardStyle=modern ; No need to change
UninstallFilesDir=Uninstall\exe\{#MyAppName} ; No need to change

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl" ; Add more languages if needed

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked ; Change if you want to add more tasks

[Files]
; Add your application files here
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\business.db"; DestDir: "{commonappdata}\{#MyAppName}"; Flags: ignoreversion; Permissions: users-modify ; Change the source path
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion ; Change the source path
Source: "C:\Users\pc\Desktop\fish_dealer_software\logo.ico"; DestDir: "{app}"; Flags: ignoreversion ; Change the source path
Source: "C:\Users\pc\Desktop\fish_dealer_software\logo.bmp"; DestDir: "{app}"; Flags: ignoreversion ; Change the source path
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\icons\*.svg"; DestDir: "{app}\icons"; Flags: ignoreversion ; Change the source path
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\images\*.png"; DestDir: "{app}\images"; Flags: ignoreversion ; Change the source path

[Registry]
; Modify file associations if needed
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
; Add shortcuts here
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\logo.ico" ; Change the icon path if needed
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\logo.ico"; Tasks: desktopicon ; Change the icon path if needed

[Run]
; Add post-install actions here
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
```
### Run 
```
Now simply run for packing software
```
