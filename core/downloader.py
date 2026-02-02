import yt_dlp
import os
import threading
import time
from datetime import datetime

class YTDownloader:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.is_cancelled = False

    def get_info(self, url):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return info
            except Exception as e:
                return {"error": str(e)}

    def download(self, url, options):
        """
        options: {
            'format_id': 'bestvideo+bestaudio/best',
            'outtmpl': 'path/to/file.%(ext)s',
            'postprocessors': [...],
            'subtitles': True/False,
            'ext': 'mp4'
        }
        """
        self.is_cancelled = False
        
        def progress_hook(d):
            if self.is_cancelled:
                raise Exception("Download cancelled by user")
            
            if d['status'] == 'downloading':
                p = d.get('_percent_str', '0%').replace('%','')
                try:
                    percent = float(p)
                except:
                    percent = 0.0
                
                speed = d.get('_speed_str', '0MB/s')
                eta = d.get('_eta_str', '00:00')
                
                # Get total size for stats
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                size_mb = total_bytes / (1024 * 1024) if total_bytes else 0
                
                if self.progress_callback:
                    self.progress_callback({
                        'percent': percent,
                        'speed': speed,
                        'eta': eta,
                        'status': 'downloading',
                        'filename': os.path.basename(d.get('filename', '')),
                        'size_mb': size_mb
                    })

        ydl_opts = {
            'format': options.get('format_id', 'best'),
            'outtmpl': options.get('outtmpl', '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'noplaylist': options.get('noplaylist', True),
            'merge_output_format': options.get('ext', 'mp4'),
        }

        if options.get('subtitles'):
            ydl_opts['writesubtitles'] = True
            ydl_opts['allsubtitles'] = True
            ydl_opts['writeautomaticsub'] = True

        if options.get('postprocessors'):
            ydl_opts['postprocessors'] = options.get('postprocessors')

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                if self.progress_callback:
                    self.progress_callback({'status': 'finished', 'percent': 100})
                return True
        except Exception as e:
            if "cancelled" in str(e):
                return "cancelled"
            return str(e)

    def cancel(self):
        self.is_cancelled = True
