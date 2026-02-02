# YouTube Downloader Pro

A professional, fully-featured desktop application for downloading YouTube videos and playlists.

## Features
- **No Subscription**: Full access to all features immediately.
- **High Quality**: Download up to 4K resolution.
- **Multiple Formats**: MP4, MKV, MP3, WAV, M4A.
- **Playlist Support**: Download entire playlists with one click.
- **Real-time Stats**: Track download speed, percentage, and ETA.
- **History & Analytics**: View your download history and visual charts of your activity.
- **Modern UI**: Clean, dark-themed interface built with CustomTkinter.

## Project Structure
- `main.py`: Entry point.
- `core/`: Backend logic (yt-dlp integration, stats management).
- `ui/`: Frontend components (frames for each section).
- `utils/`: Helper classes (settings management).
- `build_exe.py`: Script to create a standalone executable.

## Development Setup
1. Install dependencies:
   ```bash
   pip install yt-dlp customtkinter pillow matplotlib pandas requests pyinstaller
   ```
2. Run the application:
   ```bash
   python main.py
   ```

## Building for Windows
Follow the instructions in `INSTALLER_GUIDE.md` to create a standalone EXE and a professional installer.
