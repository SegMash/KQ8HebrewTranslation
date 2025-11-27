# Building the KQ8 Hebrew Translation Installer

## Prerequisites

1. **NSIS (Nullsoft Scriptable Install System)**
   - Download from: https://nsis.sourceforge.io/Download
   - Install NSIS on your Windows machine

## Preparing the Build

1. Make sure you have run `translate_game.cmd` successfully to generate all patch files in the `.\patch\` directory

2. Verify that the following directory structure exists:
   ```
   .\patch\
   ├── GAME\
   │   ├── 8Gui\
   │   │   ├── consoleg.pft
   │   │   ├── consoles.pft
   │   │   ├── consolel.pft
   │   │   ├── 20.pft
   │   │   ├── 20sl.pft
   │   │   ├── 27.pft
   │   │   ├── 27sl.pft
   │   │   ├── 36.pft
   │   │   ├── 36sl.pft
   │   │   ├── 45.pft
   │   │   ├── 45sl.pft
   │   │   └── main18.pbm
   │   └── English\
   │       ├── 0.MSG
   │       └── 500.MSG
   ├── daventry\
   │   ├── 8gui\
   │   │   └── console.pft
   │   └── English\
   │       └── 1000.MSG
   ├── deadcity\
   ├── swamp\
   ├── gnome\
   ├── barren\
   ├── iceworld\
   ├── temple1\
   └── temple2\
   ```

## Building the Installer

### Option 1: Using NSIS GUI (MakeNSISW)

1. Right-click on `KQ8_Hebrew_Patch.nsi`
2. Select "Compile NSIS Script"
3. The installer `KQ8_Hebrew_Patch_Setup.exe` will be created in the same directory

### Option 2: Using Command Line

1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```
   cd C:\WS\KQ8HebrewTranslation
   ```
3. Run NSIS compiler:
   ```
   "C:\Program Files (x86)\NSIS\makensis.exe" KQ8_Hebrew_Patch.nsi
   ```
4. The installer `KQ8_Hebrew_Patch_Setup.exe` will be created

## Distributing the Installer

Once built, you can distribute `KQ8_Hebrew_Patch_Setup.exe` to users.

### Installation Process for Users:

1. Run `KQ8_Hebrew_Patch_Setup.exe`
2. Accept the license agreement
3. Select the KQ8 installation directory (default: C:\Games\KQ8)
4. Click Install
5. The installer will:
   - Back up original game files to `__Hebrew_Patch_Backup__` folder
   - Copy Hebrew translation files to the game directory

### Uninstallation:

1. Run the uninstaller from:
   - Start Menu → KQ8 Hebrew Translation Patch → Uninstall
   - Or directly: `C:\Games\KQ8\uninst.exe`
2. The uninstaller will:
   - Restore all original game files from backup
   - Remove the backup directory
   - Remove the uninstaller

## Notes

- The installer requires administrator privileges to modify game files
- Original files are safely backed up before any modifications
- Users can restore the original game at any time using the uninstaller
- The installer only patches game text and font files - no executable modifications

## Troubleshooting

**Problem**: Installer fails to compile
- **Solution**: Ensure NSIS is properly installed and all files in `.\patch\` directory exist

**Problem**: "File not found" error during compilation
- **Solution**: Check that all referenced files in the .nsi script exist in the `.\patch\` directory

**Problem**: Installer doesn't detect KQ8 installation
- **Solution**: Users should manually browse to their KQ8 installation directory during installation
