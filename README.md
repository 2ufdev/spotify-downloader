# 🎵 Spotify Artist Downloader

A Python script that downloads **all tracks from a Spotify artist** by fetching metadata from **Spotify API** and downloading matching audio from **YouTube** as `.mp3`.

---

## ⚙️ Features
- 🔍 Search any artist on Spotify  
- 💿 Retrieve all albums and singles  
- 🎧 Download each track automatically from YouTube  
- 🔄 Convert audio to high-quality `.mp3` (192 kbps)  
- 📂 Save all files in the `downloads/` directory  

---

## 🧩 Installation

### 1. Clone the repository
```bash
git clone https://github.com/2ufdev/spotify-downloader.git
cd spotify-downloader
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Spotify credentials

Edit the top of the script and replace:

```python
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
```

You can get these from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

---

## 🚀 Usage

```bash
python main.py
```

Then enter the artist name when prompted:

```
Artist Name (ex. : Daft Punk) :
```

All tracks will be downloaded into the `downloads/` folder.

---

## 🧠 Requirements

* Python 3.8+
* `spotipy`
* `yt-dlp`
* `ffmpeg` (must be installed and in PATH)

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.
Downloading copyrighted material may violate the terms of service of YouTube or Spotify. Use responsibly.
