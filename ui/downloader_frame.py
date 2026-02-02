import customtkinter as ctk
import threading
import requests
import os
from PIL import Image
from io import BytesIO
from core.downloader import YTDownloader
from utils.settings import Settings
from core.stats_manager import StatsManager

class DownloaderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        self.settings = Settings()
        self.stats_manager = StatsManager()
        self.downloader = YTDownloader(progress_callback=self.update_progress)
        
        # URL Entry
        self.url_label = ctk.CTkLabel(self, text="Enter YouTube Video or Playlist URL:", font=ctk.CTkFont(size=14))
        self.url_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.url_entry = ctk.CTkEntry(self, placeholder_text="https://www.youtube.com/watch?v=...", height=35)
        self.url_entry.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.url_entry.bind("<Return>", lambda e: self.fetch_info())
        
        self.fetch_button = ctk.CTkButton(self, text="Analyze URL", command=self.fetch_info)
        self.fetch_button.grid(row=1, column=1, padx=(0, 20), pady=5)

        # Preview Area
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.preview_frame.grid_columnconfigure(1, weight=1)
        
        self.thumbnail_label = ctk.CTkLabel(self.preview_frame, text="No Preview", width=200, height=120, fg_color="gray30")
        self.thumbnail_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.info_label = ctk.CTkLabel(self.preview_frame, text="Enter a URL to see video details", justify="left", anchor="w")
        self.info_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Options Area
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        # Video Quality
        self.quality_label = ctk.CTkLabel(self.options_frame, text="Video Quality:")
        self.quality_label.grid(row=0, column=0, padx=10, pady=10)
        self.video_qualities = ["Best", "8K (4320p)", "4K (2160p)", "2K (1440p)", "1080p", "720p", "480p", "360p", "240p", "144p", "Audio Only"]
        self.quality_combo = ctk.CTkComboBox(self.options_frame, values=self.video_qualities)
        self.quality_combo.grid(row=0, column=1, padx=10, pady=10)
        self.quality_combo.set("Best")
        
        # Audio Bitrate
        self.audio_label = ctk.CTkLabel(self.options_frame, text="Audio Bitrate:")
        self.audio_label.grid(row=0, column=2, padx=10, pady=10)
        self.audio_bitrates = ["320kbps", "256kbps", "192kbps", "128kbps", "64kbps"]
        self.audio_combo = ctk.CTkComboBox(self.options_frame, values=self.audio_bitrates)
        self.audio_combo.grid(row=0, column=3, padx=10, pady=10)
        self.audio_combo.set("192kbps")
        
        # Format
        self.format_label = ctk.CTkLabel(self.options_frame, text="Format:")
        self.format_label.grid(row=1, column=0, padx=10, pady=10)
        self.format_combo = ctk.CTkComboBox(self.options_frame, values=["MP4", "MKV", "MP3", "WAV", "M4A"])
        self.format_combo.grid(row=1, column=1, padx=10, pady=10)
        self.format_combo.set("MP4")

        # Progress Area
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(self, text="Ready")
        self.status_label.grid(row=5, column=0, columnspan=2, padx=20, pady=5)

        # Action Buttons
        self.download_button = ctk.CTkButton(self, text="Download Now", command=self.start_download, state="disabled", height=40, font=ctk.CTkFont(weight="bold"))
        self.download_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20)

        self.current_video_info = None
        self.last_download_size = 0

    def fetch_info(self):
        url = self.url_entry.get()
        if not url: return
        
        self.status_label.configure(text="Fetching video info...")
        self.fetch_button.configure(state="disabled")
        
        def thread_func():
            info = self.downloader.get_info(url)
            self.after(0, lambda: self.display_info(info))
            
        threading.Thread(target=thread_func, daemon=True).start()

    def display_info(self, info):
        self.fetch_button.configure(state="normal")
        if "error" in info:
            self.status_label.configure(text=f"Error: {info['error']}")
            return
        
        self.current_video_info = info
        title = info.get('title', 'Unknown Title')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown')
        
        info_text = f"Title: {title}\nUploader: {uploader}\n"
        if 'entries' in info:
            info_text += f"Playlist: {len(info['entries'])} videos"
        else:
            info_text += f"Duration: {duration // 60}:{duration % 60:02d}"
            
        self.info_label.configure(text=info_text)
        self.status_label.configure(text="Ready to download")
        self.download_button.configure(state="normal")
        
        # Load thumbnail
        thumb_url = info.get('thumbnail')
        if thumb_url:
            threading.Thread(target=self.load_thumbnail, args=(thumb_url,), daemon=True).start()

    def load_thumbnail(self, url):
        try:
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            ctk_img = ctk.CTkImage(img, size=(200, 120))
            self.after(0, lambda: self.thumbnail_label.configure(image=ctk_img, text=""))
        except:
            pass

    def start_download(self):
        url = self.url_entry.get()
        quality = self.quality_combo.get()
        bitrate = self.audio_combo.get().replace('kbps', '')
        fmt = self.format_combo.get().lower()
        
        options = {
            'outtmpl': os.path.join(self.settings.get('download_path'), '%(title)s.%(ext)s'),
            'ext': fmt if fmt in ['mp4', 'mkv'] else 'mp4'
        }
        
        # Smart Quality Selection
        if quality == "Audio Only" or fmt in ['mp3', 'wav', 'm4a']:
            options['format_id'] = 'bestaudio/best'
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': fmt if fmt in ['mp3', 'wav', 'm4a'] else 'mp3',
                'preferredquality': bitrate,
            }]
        else:
            # Map quality to height
            height_map = {
                "8K (4320p)": "4320", "4K (2160p)": "2160", "2K (1440p)": "1440",
                "1080p": "1080", "720p": "720", "480p": "480", "360p": "360",
                "240p": "240", "144p": "144"
            }
            if quality in height_map:
                h = height_map[quality]
                options['format_id'] = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"
            else:
                options['format_id'] = 'bestvideo+bestaudio/best'
            
        self.download_button.configure(state="disabled")
        self.status_label.configure(text="Starting download...")
        self.last_download_size = 0
        
        def thread_func():
            result = self.downloader.download(url, options)
            self.after(0, lambda: self.download_finished(result))
            
        threading.Thread(target=thread_func, daemon=True).start()

    def update_progress(self, data):
        if data['status'] == 'downloading':
            self.last_download_size = data.get('size_mb', 0)
            self.after(0, lambda: self._update_ui(data))
        elif data['status'] == 'finished':
            self.after(0, lambda: self.progress_bar.set(1.0))

    def _update_ui(self, data):
        self.progress_bar.set(data['percent'] / 100)
        self.status_label.configure(text=f"Downloading: {data['percent']}% | Speed: {data['speed']} | ETA: {data['eta']}")

    def download_finished(self, result):
        self.download_button.configure(state="normal")
        if result is True:
            self.status_label.configure(text="Download Completed Successfully!")
            if self.current_video_info:
                self.stats_manager.add_history({
                    'title': self.current_video_info.get('title', 'Unknown'),
                    'thumbnail': self.current_video_info.get('thumbnail', ''),
                    'quality': self.quality_combo.get(),
                    'format': self.format_combo.get(),
                    'size_mb': self.last_download_size
                })
        elif result == "cancelled":
            self.status_label.configure(text="Download Cancelled")
        else:
            self.status_label.configure(text=f"Error: {result}")
