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
## Generate Certificate with Powershell
```bash
New-SelfSignedCertificate -Type Custom -Subject "CN=Sofmake, O=Sofmake, C=US" -KeyUsage DigitalSignature -FriendlyName "My Friendly Cert Name" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

Get-ChildItem -Path Cert:\CurrentUser\My  # to see 

$thumb = "F2D86ADFA91BEEBF4EAF870B406DF5D7F373075E"
$cert = Get-Item "Cert:\CurrentUser\My\$thumb"
Export-PfxCertificate -Cert $cert -FilePath "C:\Users\pc\Desktop\fish_dealer_software\output\MyCertbing.pfx" -Password (Read-Host -AsSecureString "Enter password")
```
- Input password example: 1234
## Apply Certificate
```
- open signgui Software
- C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe (Eample : SingTool location)
- C:\Users\pc\Desktop\fish_dealer_software\output\MyCertbing.pfx (PFX file, password : given example `1234` password to generate file)
- http://timestamp.sectigo.com (Example: timestamp Services)
- C:\Users\pc\Desktop\fish_dealer_software\output\app.exe (Output)
- SHA 256 (Signurate)
- Press `SingFile` Buttom
```
## Install Certificate
```
- from app.exe file, right click and open Properties
- Go Digital Signature
- Click on Signature from - Signature List
- Then Click Details
- Then Click `View Certificate`
- Then Click `Install Certificate`
- Then Click on `Current User`
- Then Click on `All Certificates in the following store`
- Then Opne `Certificate Store` browse file
- Then Select `Trusted Root Certification Authorities`
- Then Click `Next` and Finish
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
