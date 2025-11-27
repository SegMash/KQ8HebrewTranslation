; NSIS Installer Script for KQ8 Hebrew Translation Patch
; This installer patches King's Quest: Mask of Eternity with Hebrew translation
; It backs up original files and allows restoration via uninstaller

!define PRODUCT_NAME "KQ8 Hebrew Translation Patch"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "Hebrew Adventure"
!define PRODUCT_WEB_SITE "https://github.com/SegMash/KQ8HebrewTranslation"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI Settings
!include "MUI2.nsh"
!include "FileFunc.nsh"

!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME

; License page
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"

; Directory page - ask for KQ8 installation directory
!define MUI_DIRECTORYPAGE_TEXT_TOP "Please select your King's Quest: Mask of Eternity installation folder.$\r$\n$\r$\nThe installer will patch the game files with Hebrew translation."
!define MUI_DIRECTORYPAGE_TEXT_DESTINATION "KQ8 Installation Folder"
!insertmacro MUI_PAGE_DIRECTORY

; Instfiles page
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!define MUI_FINISHPAGE_TITLE "Hebrew Translation Installed Successfully"
!define MUI_FINISHPAGE_TEXT "King's Quest: Mask of Eternity has been patched with Hebrew translation.$\r$\n$\r$\nYou can now launch the game and enjoy it in Hebrew!"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language
!insertmacro MUI_LANGUAGE "English"

; Installer attributes
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "KQ8_Hebrew_Patch_Setup.exe"
InstallDir "C:\Games\KQ8"
InstallDirRegKey HKLM "${PRODUCT_UNINST_KEY}" "InstallLocation"
ShowInstDetails show
ShowUnInstDetails show

; Request admin rights
RequestExecutionLevel admin

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  
  ; Create backup directory
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__"
  
  DetailPrint "Backing up and patching game files..."
  
  ; Backup and patch GAME folder
  Call PatchGAME
  
  ; Backup and patch location folders
  Call PatchDaventry
  Call PatchCastled
  Call PatchDeadcity
  Call PatchSwamp
  Call PatchGnome
  Call PatchBarren
  Call PatchIceworld
  Call PatchSnowexit
  Call PatchTemple1
  Call PatchTemple2
  Call PatchTemple3
  Call PatchTemple4
  
  DetailPrint "Patch installation completed!"
  
SectionEnd

; Function to patch GAME folder
Function PatchGAME
  DetailPrint "Patching GAME folder..."
  
  ; Create backup directory for GAME
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\GAME\English"
  
  ; Backup and replace font files in GAME\8Gui
  IfFileExists "$INSTDIR\GAME\8Gui\consoleg.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\consoleg.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consoleg.pft"
    File "/oname=$INSTDIR\GAME\8Gui\consoleg.pft" "patch\GAME\8Gui\consoleg.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\consoles.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\consoles.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consoles.pft"
    File "/oname=$INSTDIR\GAME\8Gui\consoles.pft" "patch\GAME\8Gui\consoles.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\consolel.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\consolel.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consolel.pft"
    File "/oname=$INSTDIR\GAME\8Gui\consolel.pft" "patch\GAME\8Gui\consolel.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\20.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\20.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\20.pft"
    File "/oname=$INSTDIR\GAME\8Gui\20.pft" "patch\GAME\8Gui\20.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\20sl.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\20sl.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\20sl.pft"
    File "/oname=$INSTDIR\GAME\8Gui\20sl.pft" "patch\GAME\8Gui\20sl.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\27.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\27.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\27.pft"
    File "/oname=$INSTDIR\GAME\8Gui\27.pft" "patch\GAME\8Gui\27.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\27sl.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\27sl.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\27sl.pft"
    File "/oname=$INSTDIR\GAME\8Gui\27sl.pft" "patch\GAME\8Gui\27sl.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\36.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\36.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\36.pft"
    File "/oname=$INSTDIR\GAME\8Gui\36.pft" "patch\GAME\8Gui\36.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\36sl.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\36sl.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\36sl.pft"
    File "/oname=$INSTDIR\GAME\8Gui\36sl.pft" "patch\GAME\8Gui\36sl.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\45.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\45.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\45.pft"
    File "/oname=$INSTDIR\GAME\8Gui\45.pft" "patch\GAME\8Gui\45.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\45sl.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\45sl.pft" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\45sl.pft"
    File "/oname=$INSTDIR\GAME\8Gui\45sl.pft" "patch\GAME\8Gui\45sl.pft"
  
  IfFileExists "$INSTDIR\GAME\8Gui\main18.pbm" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\8Gui\main18.pbm" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\main18.pbm"
    File "/oname=$INSTDIR\GAME\8Gui\main18.pbm" "patch\GAME\8Gui\main18.pbm"
  
  ; Backup and replace MSG files in GAME\English
  IfFileExists "$INSTDIR\GAME\English\0.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\English\0.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\English\0.MSG"
    File "/oname=$INSTDIR\GAME\English\0.MSG" "patch\GAME\English\0.MSG"
  
  IfFileExists "$INSTDIR\GAME\English\500.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\GAME\English\500.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\GAME\English\500.MSG"
    File "/oname=$INSTDIR\GAME\English\500.MSG" "patch\GAME\English\500.MSG"
  
FunctionEnd

; Function to patch daventry
Function PatchDaventry
  DetailPrint "Patching daventry folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\daventry\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\daventry\English"
  IfFileExists "$INSTDIR\daventry\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\daventry\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\daventry\8gui\console.pft"
    File "/oname=$INSTDIR\daventry\8gui\console.pft" "patch\daventry\8gui\console.pft"
  IfFileExists "$INSTDIR\daventry\English\1000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\daventry\English\1000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\daventry\English\1000.MSG"
    File "/oname=$INSTDIR\daventry\English\1000.MSG" "patch\daventry\English\1000.MSG"
FunctionEnd

Function PatchCastled
  DetailPrint "Patching castled folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\castled\8gui"
  IfFileExists "$INSTDIR\castled\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\castled\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\castled\8gui\console.pft"
    File "/oname=$INSTDIR\castled\8gui\console.pft" "patch\castled\8gui\console.pft"
FunctionEnd

Function PatchDeadcity
  DetailPrint "Patching deadcity folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\English"
  IfFileExists "$INSTDIR\deadcity\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\deadcity\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\8gui\console.pft"
    File "/oname=$INSTDIR\deadcity\8gui\console.pft" "patch\deadcity\8gui\console.pft"
  IfFileExists "$INSTDIR\deadcity\English\2000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\deadcity\English\2000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\English\2000.MSG"
    File "/oname=$INSTDIR\deadcity\English\2000.MSG" "patch\deadcity\English\2000.MSG"
FunctionEnd

Function PatchSwamp
  DetailPrint "Patching swamp folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\swamp\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\swamp\English"
  IfFileExists "$INSTDIR\swamp\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\swamp\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\swamp\8gui\console.pft"
    File "/oname=$INSTDIR\swamp\8gui\console.pft" "patch\swamp\8gui\console.pft"
  IfFileExists "$INSTDIR\swamp\English\3000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\swamp\English\3000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\swamp\English\3000.MSG"
    File "/oname=$INSTDIR\swamp\English\3000.MSG" "patch\swamp\English\3000.MSG"
FunctionEnd

Function PatchGnome
  DetailPrint "Patching gnome folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\gnome\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\gnome\English"
  IfFileExists "$INSTDIR\gnome\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\gnome\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\gnome\8gui\console.pft"
    File "/oname=$INSTDIR\gnome\8gui\console.pft" "patch\gnome\8gui\console.pft"
  IfFileExists "$INSTDIR\gnome\English\4000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\gnome\English\4000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\gnome\English\4000.MSG"
    File "/oname=$INSTDIR\gnome\English\4000.MSG" "patch\gnome\English\4000.MSG"
FunctionEnd

Function PatchBarren
  DetailPrint "Patching barren folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\barren\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\barren\English"
  IfFileExists "$INSTDIR\barren\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\barren\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\barren\8gui\console.pft"
    File "/oname=$INSTDIR\barren\8gui\console.pft" "patch\barren\8gui\console.pft"
  IfFileExists "$INSTDIR\barren\English\5000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\barren\English\5000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\barren\English\5000.MSG"
    File "/oname=$INSTDIR\barren\English\5000.MSG" "patch\barren\English\5000.MSG"
FunctionEnd

Function PatchIceworld
  DetailPrint "Patching iceworld folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\English"
  IfFileExists "$INSTDIR\iceworld\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\iceworld\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\8gui\console.pft"
    File "/oname=$INSTDIR\iceworld\8gui\console.pft" "patch\iceworld\8gui\console.pft"
  IfFileExists "$INSTDIR\iceworld\English\6000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\iceworld\English\6000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\English\6000.MSG"
    File "/oname=$INSTDIR\iceworld\English\6000.MSG" "patch\iceworld\English\6000.MSG"
FunctionEnd

Function PatchSnowexit
  DetailPrint "Patching snowexit folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\snowexit\8gui"
  IfFileExists "$INSTDIR\snowexit\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\snowexit\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\snowexit\8gui\console.pft"
    File "/oname=$INSTDIR\snowexit\8gui\console.pft" "patch\snowexit\8gui\console.pft"
FunctionEnd

Function PatchTemple1
  DetailPrint "Patching temple1 folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\temple1\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\temple1\English"
  IfFileExists "$INSTDIR\temple1\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\temple1\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\temple1\8gui\console.pft"
    File "/oname=$INSTDIR\temple1\8gui\console.pft" "patch\temple1\8gui\console.pft"
  IfFileExists "$INSTDIR\temple1\English\7000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\temple1\English\7000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\temple1\English\7000.MSG"
    File "/oname=$INSTDIR\temple1\English\7000.MSG" "patch\temple1\English\7000.MSG"
FunctionEnd

Function PatchTemple2
  DetailPrint "Patching temple2 folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\temple2\8gui"
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\temple2\English"
  IfFileExists "$INSTDIR\temple2\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\temple2\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\temple2\8gui\console.pft"
    File "/oname=$INSTDIR\temple2\8gui\console.pft" "patch\temple2\8gui\console.pft"
  IfFileExists "$INSTDIR\temple2\English\7000.MSG" 0 +3
    CopyFiles /SILENT "$INSTDIR\temple2\English\7000.MSG" "$INSTDIR\__Hebrew_Patch_Backup__\temple2\English\7000.MSG"
    File "/oname=$INSTDIR\temple2\English\7000.MSG" "patch\temple2\English\7000.MSG"
FunctionEnd

Function PatchTemple3
  DetailPrint "Patching temple3 folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\temple3\8gui"
  IfFileExists "$INSTDIR\temple3\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\temple3\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\temple3\8gui\console.pft"
    File "/oname=$INSTDIR\temple3\8gui\console.pft" "patch\temple3\8gui\console.pft"
FunctionEnd

Function PatchTemple4
  DetailPrint "Patching temple4 folder..."
  CreateDirectory "$INSTDIR\__Hebrew_Patch_Backup__\temple4\8gui"
  IfFileExists "$INSTDIR\temple4\8gui\console.pft" 0 +3
    CopyFiles /SILENT "$INSTDIR\temple4\8gui\console.pft" "$INSTDIR\__Hebrew_Patch_Backup__\temple4\8gui\console.pft"
    File "/oname=$INSTDIR\temple4\8gui\console.pft" "patch\temple4\8gui\console.pft"
FunctionEnd

Section -AdditionalIcons
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "$INSTDIR\KQ8_Hebrew_Uninstaller.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\KQ8_Hebrew_Uninstaller.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\KQ8_Hebrew_Uninstaller.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "InstallLocation" "$INSTDIR"
SectionEnd

; Uninstaller Section
Section Uninstall
  DetailPrint "Restoring original game files..."
  
  ; Restore GAME folder files
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consoleg.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consoleg.pft" "$INSTDIR\GAME\8Gui\consoleg.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consoles.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consoles.pft" "$INSTDIR\GAME\8Gui\consoles.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consolel.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\consolel.pft" "$INSTDIR\GAME\8Gui\consolel.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\20.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\20.pft" "$INSTDIR\GAME\8Gui\20.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\20sl.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\20sl.pft" "$INSTDIR\GAME\8Gui\20sl.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\27.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\27.pft" "$INSTDIR\GAME\8Gui\27.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\27sl.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\27sl.pft" "$INSTDIR\GAME\8Gui\27sl.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\36.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\36.pft" "$INSTDIR\GAME\8Gui\36.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\36sl.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\36sl.pft" "$INSTDIR\GAME\8Gui\36sl.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\45.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\45.pft" "$INSTDIR\GAME\8Gui\45.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\45sl.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\45sl.pft" "$INSTDIR\GAME\8Gui\45sl.pft"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\main18.pbm" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\8Gui\main18.pbm" "$INSTDIR\GAME\8Gui\main18.pbm"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\English\0.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\English\0.MSG" "$INSTDIR\GAME\English\0.MSG"
  
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\GAME\English\500.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\GAME\English\500.MSG" "$INSTDIR\GAME\English\500.MSG"
  
  ; Restore location folders
  Call un.RestoreDaventry
  Call un.RestoreCastled
  Call un.RestoreDeadcity
  Call un.RestoreSwamp
  Call un.RestoreGnome
  Call un.RestoreBarren
  Call un.RestoreIceworld
  Call un.RestoreSnowexit
  Call un.RestoreTemple1
  Call un.RestoreTemple2
  Call un.RestoreTemple3
  Call un.RestoreTemple4
  
  ; Remove backup directory
  RMDir /r "$INSTDIR\__Hebrew_Patch_Backup__"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${PRODUCT_NAME}"
  
  ; Remove uninstaller
  Delete "$INSTDIR\KQ8_Hebrew_Uninstaller.exe"
  
  ; Remove registry keys
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  
  SetAutoClose true
  
  DetailPrint "Original game files have been restored!"
SectionEnd

; Uninstaller functions to restore location files
Function un.RestoreDaventry
  DetailPrint "Restoring daventry folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\daventry\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\daventry\8gui\console.pft" "$INSTDIR\daventry\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\daventry\English\1000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\daventry\English\1000.MSG" "$INSTDIR\daventry\English\1000.MSG"
FunctionEnd

Function un.RestoreCastled
  DetailPrint "Restoring castled folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\castled\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\castled\8gui\console.pft" "$INSTDIR\castled\8gui\console.pft"
FunctionEnd

Function un.RestoreDeadcity
  DetailPrint "Restoring deadcity folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\8gui\console.pft" "$INSTDIR\deadcity\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\English\2000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\deadcity\English\2000.MSG" "$INSTDIR\deadcity\English\2000.MSG"
FunctionEnd

Function un.RestoreSwamp
  DetailPrint "Restoring swamp folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\swamp\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\swamp\8gui\console.pft" "$INSTDIR\swamp\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\swamp\English\3000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\swamp\English\3000.MSG" "$INSTDIR\swamp\English\3000.MSG"
FunctionEnd

Function un.RestoreGnome
  DetailPrint "Restoring gnome folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\gnome\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\gnome\8gui\console.pft" "$INSTDIR\gnome\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\gnome\English\4000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\gnome\English\4000.MSG" "$INSTDIR\gnome\English\4000.MSG"
FunctionEnd

Function un.RestoreBarren
  DetailPrint "Restoring barren folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\barren\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\barren\8gui\console.pft" "$INSTDIR\barren\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\barren\English\5000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\barren\English\5000.MSG" "$INSTDIR\barren\English\5000.MSG"
FunctionEnd

Function un.RestoreIceworld
  DetailPrint "Restoring iceworld folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\8gui\console.pft" "$INSTDIR\iceworld\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\English\6000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\iceworld\English\6000.MSG" "$INSTDIR\iceworld\English\6000.MSG"
FunctionEnd

Function un.RestoreSnowexit
  DetailPrint "Restoring snowexit folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\snowexit\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\snowexit\8gui\console.pft" "$INSTDIR\snowexit\8gui\console.pft"
FunctionEnd

Function un.RestoreTemple1
  DetailPrint "Restoring temple1 folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\temple1\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\temple1\8gui\console.pft" "$INSTDIR\temple1\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\temple1\English\7000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\temple1\English\7000.MSG" "$INSTDIR\temple1\English\7000.MSG"
FunctionEnd

Function un.RestoreTemple2
  DetailPrint "Restoring temple2 folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\temple2\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\temple2\8gui\console.pft" "$INSTDIR\temple2\8gui\console.pft"
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\temple2\English\7000.MSG" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\temple2\English\7000.MSG" "$INSTDIR\temple2\English\7000.MSG"
FunctionEnd

Function un.RestoreTemple3
  DetailPrint "Restoring temple3 folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\temple3\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\temple3\8gui\console.pft" "$INSTDIR\temple3\8gui\console.pft"
FunctionEnd

Function un.RestoreTemple4
  DetailPrint "Restoring temple4 folder..."
  IfFileExists "$INSTDIR\__Hebrew_Patch_Backup__\temple4\8gui\console.pft" 0 +2
    CopyFiles /SILENT "$INSTDIR\__Hebrew_Patch_Backup__\temple4\8gui\console.pft" "$INSTDIR\temple4\8gui\console.pft"
FunctionEnd
