# YouTube Downloader Pro - Installer Creation Guide

This guide explains how to create a professional Windows installer for the YouTube Downloader Pro application using **Inno Setup**.

## Prerequisites
1. **Inno Setup**: Download and install from [jrsoftware.org](https://jrsoftware.org/isdl.php).
2. **FFmpeg**: Download the FFmpeg shared/static build for Windows and place `ffmpeg.exe` and `ffprobe.exe` in the `assets/` folder before building the EXE.

## Step 1: Build the Executable
Run the build script to generate the standalone `.exe` file:
```bash
python build_exe.py
```
The output will be in the `dist/YTDownloaderPro.exe` folder.

## Step 2: Create Inno Setup Script
Create a file named `installer_script.iss` with the following content:

```pascal
[Setup]
AppName=YouTube Downloader Pro
AppVersion=1.0
DefaultDirName={autopf}\YouTube Downloader Pro
DefaultGroupName=YouTube Downloader Pro
UninstallDisplayIcon={app}\YTDownloaderPro.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer_output

[Files]
Source: "dist\YTDownloaderPro.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include FFmpeg if not bundled in EXE
Source: "assets\ffmpeg.exe"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\ffprobe.exe"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
Name: "{group}\YouTube Downloader Pro"; Filename: "{app}\YTDownloaderPro.exe"
Name: "{autodesktop}\YouTube Downloader Pro"; Filename: "{app}\YTDownloaderPro.exe"

[Run]
Filename: "{app}\YTDownloaderPro.exe"; Description: "Launch YouTube Downloader Pro"; Flags: nowait postinstall skipifsilent
```

## Step 3: Compile the Installer
1. Open **Inno Setup Compiler**.
2. Load the `installer_script.iss` file.
3. Click **Build > Compile**.
4. Your professional installer will be generated in the `installer_output` folder.

## Note on FFmpeg
The application requires FFmpeg for format conversions (like MP3). Ensure the `ffmpeg.exe` is either in the same directory as the app or in the `assets` folder as specified in the installer script.
