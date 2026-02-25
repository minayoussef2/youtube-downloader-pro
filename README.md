# 🎬 YouTube Downloader Pro

A powerful, feature-rich desktop video downloader built with Python and CustomTkinter. Download YouTube videos, playlists, and HLS/M3U8 streams — all from a clean, modern dark-mode interface.

---

## ✨ Features at a Glance

| Feature | Details |
|---|---|
| YouTube Downloads | Videos, playlists, or mixed URL queues |
| HLS / M3U8 Downloads | BunnyCDN, CDN-protected streams, direct `.m3u8` links |
| Multi-link Queue | Paste multiple URLs at once and manage them as a queue |
| Pause & Resume | Pause any download mid-way and resume it later |
| IDM-style Speed Boost | Split downloads into parallel connections (1–16) |
| Quality Selection | From 144p up to 8K, or Audio Only |
| Estimated File Size | See the estimated size before you download |
| Format Choice | MP4, MKV, MP3, WAV, M4A |
| Download History | Browse past downloads with timestamps and metadata |
| Statistics | Track total videos downloaded and data consumed |
| Settings | Theme, download folder, default quality, connection count |

---

## 📦 Requirements

Before running the app, install the required dependencies:

```bash
pip install customtkinter yt-dlp Pillow requests
```

You also need **FFmpeg** installed and available in your system PATH:

- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org) or run `winget install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

---

## 🚀 Running the App

```bash
cd yt_downloader_pro_v2
python main.py
```

---

## 🗂️ Navigation

The app has a sidebar with five sections:

- **▶ YT Downloader** — Download YouTube videos and playlists
- **🔗 HLS Downloader** — Download CDN-hosted `.m3u8` streams
- **🕓 History** — View your past downloads
- **📊 Statistics** — See overall download stats
- **⚙ Settings** — Configure the app behavior

---

## ▶ YT Downloader

The YouTube tab supports downloading single videos, full playlists, and any combination of both at the same time through a queue system.

### How to use

1. Paste one or more YouTube URLs into the text box — one URL per line. You can mix video links and playlist links freely.
2. Click **➕ Add to Queue**. The app will automatically detect playlists and expand them into individual video items.
3. Each item in the queue will show the video thumbnail, title, duration, uploader, and view count once analyzed.
4. Choose your preferred **Quality**, **Format**, and the **Estimated Size** will update instantly.
5. Click **⬇ Download** on individual items, or use **⬇ Download All** to start everything at once.

### Queue controls

| Button | Action |
|---|---|
| ⬇ Download All | Start all pending items in the queue |
| ⏸ Pause All | Pause every active download |
| ✕ Cancel All | Cancel every active download |
| Sequential toggle | When checked, downloads run one at a time instead of all at once |

### Per-item controls

Each queue card has its own set of buttons:

- **⬇ Download** — Start this specific item
- **⏸ Pause / ▶ Resume** — Pause mid-download and resume at any time
- **✕ Cancel** — Cancel and discard the current download
- **✕ (top right)** — Remove the item from the queue entirely

### Supported quality options

`Best · 8K (4320p) · 4K (2160p) · 2K (1440p) · 1080p · 720p · 480p · 360p · 240p · 144p · Audio Only`

### Supported output formats

`MP4 · MKV · MP3 · WAV · M4A`

> When Audio Only or an audio format (MP3/WAV/M4A) is selected, the video stream is skipped and only the audio is extracted and converted.

---

## 🔗 HLS / M3U8 Downloader

This tab is designed for downloading HLS (HTTP Live Streaming) video streams — the kind used by CDN providers like BunnyCDN, Cloudflare Stream, and similar services. These are URLs ending in `.m3u8`.

### How to use

1. Enter the **Referer URL** — this is the website where the video is embedded. CDN providers check this header to allow or deny access. Without the correct Referer, the server will return a 403 Forbidden error.
2. Paste one or more `.m3u8` stream URLs into the text box — one per line.
3. Click **➕ Add to Queue**. Each stream will be analyzed automatically to fetch its title, duration, and available quality levels.
4. Select the **Quality** for each item. If size data is available, the **Estimated Size** will update immediately.
5. Click **Download** per item, or **⬇ Download All** to start everything.

### Per-item controls

Each HLS item card has the same controls as YT items:

- **Download / Re-download** — Start the download
- **⏸ Pause / ▶ Resume** — Pause and resume between stream fragments
- **Cancel** — Stop the current download
- **✕** — Remove the item from the queue

### Status indicators

| Icon | Meaning |
|---|---|
| ⏳ | Analyzing the stream |
| 🟢 | Ready to download |
| 🟡 | Warning (metadata unavailable, download still possible) |
| 🔵 | Currently downloading |
| ✅ | Download complete |
| 🔴 | Error occurred |

### Finding your Referer URL

Open the page where the video is hosted in your browser. Press **F12** to open DevTools, go to the **Network** tab, refresh the page, filter for `.m3u8`, and look at the **Request Headers** of that request. The `Referer` value is what you need.

---

## ⏸ Pause & Resume

Every download in both tabs supports pausing. The pause works **between stream fragments**, meaning the current fragment finishes cleanly before the download freezes. This makes resuming instant and seamless — no corrupted files, no restarting from the beginning.

This is especially useful for HLS streams which consist of hundreds or thousands of small fragments (you may have noticed `Frag 256/1737` in the progress bar — that means 1737 fragments total).

---

## ⚡ IDM-Style Multi-Connection Downloads

Found in **Settings → Multi-Connection Downloads**, this feature splits each download into multiple parallel fragment connections — similar to how Internet Download Manager (IDM) splits files into chunks to maximize download speed.

### Connection presets

| Preset | Best for |
|---|---|
| 1 — Safe | Slow or restrictive servers, avoiding rate limits |
| 4 — Balanced | Default. Good for most connections |
| 8 — Fast | Fast internet connections, permissive servers |
| 16 — Maximum | Maximum speed, may be rate-limited by some servers |

You can also use the slider to set any value from 1 to 16.

> ⚠️ Very high values (12–16) may cause some servers to rate-limit or temporarily block your IP. If you get errors or slow speeds at high settings, try reducing the connection count.

---

## 🕓 Download History

The History tab shows all completed downloads with:

- Video title
- Download timestamp
- Quality and format used
- File size (when available)

At the top of the History tab you'll find:

- **📁 Open Download Folder** — Opens your configured download directory in File Explorer
- **🗑 Clear History** — Wipes the history list

Each history entry also has an **📁 Open Folder** button to jump directly to where that file was saved.

---

## 📊 Statistics

The Statistics tab tracks:

- Total number of videos downloaded (all-time)
- Total data downloaded in MB/GB (all-time)
- Session stats (since the app was last launched)
- Daily download counts

---

## ⚙ Settings

| Setting | Description |
|---|---|
| Theme | Switch between Light, Dark, and System mode |
| Download Folder | Choose where files are saved. Default: `~/Downloads/YTDownloaderPro` |
| Default Quality | Pre-select a quality level for new queue items |
| Multi-Connection Downloads | Set the number of parallel fragment connections (1–16) |

Click **💾 Save All Settings** to persist your changes. Settings are stored in `config.json` in the app directory.

---

## 📁 File Structure

```
yt_downloader_pro_v2/
│
├── main.py                     # Entry point
├── config.json                 # Saved settings (auto-created)
│
├── core/
│   ├── downloader.py           # YTDownloader + ItemDownloader (pause/cancel engine)
│   └── stats_manager.py        # History and statistics storage
│
├── ui/
│   ├── main_window.py          # App window and sidebar navigation
│   ├── downloader_frame.py     # YouTube multi-queue downloader tab
│   ├── hls_downloader_frame.py # HLS/M3U8 multi-queue downloader tab
│   ├── history_frame.py        # Download history tab
│   ├── stats_frame.py          # Statistics tab
│   └── settings_frame.py       # Settings tab
│
└── utils/
    └── settings.py             # Settings load/save helper
```

---

## 🔧 Troubleshooting

**403 Forbidden on HLS streams**
→ Make sure you've entered the correct Referer URL in the HLS tab before adding to queue. The Referer must match the website hosting the video.

**"Requested format not available"**
→ The stream doesn't support the selected quality. Switch to **Best Available** and the app will automatically pick the best format the server offers.

**Download is very slow**
→ Increase the connection count in Settings. Try 8 or 16 for faster speeds.

**FFmpeg not found**
→ Make sure FFmpeg is installed and added to your system PATH. Restart the app after installing.

**App won't start**
→ Make sure all dependencies are installed: `pip install customtkinter yt-dlp Pillow requests`

---

## 📄 License

This project is for personal use. Please respect copyright laws and the terms of service of the platforms you download from.
