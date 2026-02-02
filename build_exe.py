import PyInstaller.__main__
import os
import shutil

def build():
    # Ensure assets exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Define build parameters
    params = [
        'main.py',
        '--name=YTDownloaderPro',
        '--onefile',
        '--windowed',
        '--add-data=assets:assets',
        '--collect-all=customtkinter',
        '--collect-all=yt_dlp',
        '--hidden-import=PIL._tkinter_finder',
    ]

    # Run PyInstaller
    PyInstaller.__main__.run(params)

    print("Build completed! Check the 'dist' folder for the executable.")

if __name__ == "__main__":
    build()
