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
ChangesAssociations=yes
DisableProgramGroupPage=yes
DisableDirPage=no
OutputBaseFilename=mysetup
SetupIconFile=C:\Users\pc\Desktop\fish_dealer_software\logo.ico
WizardSmallImageFile=C:\Users\pc\Desktop\fish_dealer_software\logo.bmp
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallFilesDir=Uninstall\exe\{#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\business.db"; DestDir: "{commonappdata}\{#MyAppName}"; Flags: ignoreversion; Permissions: users-modify
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\logo.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\logo.bmp"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\icons\*.svg"; DestDir: "{app}\icons"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\images\*.png"; DestDir: "{app}\images"; Flags: ignoreversion
Source: "C:\Users\pc\Desktop\fish_dealer_software\output\font\*.ttf"; DestDir: "{app}\font"; Flags: ignoreversion

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



add font path here


location 
font/arial.ttf
font/nato.ttf