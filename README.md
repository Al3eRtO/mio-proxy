# 🚀 EasyProxy - Universal Server Proxy for HLS Streaming

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![HLS](https://img.shields.io/badge/HLS-Streaming-red.svg)](https://developer.apple.com/streaming/)

> **A universal proxy server for HLS, M3U8, and IPTV streaming** 🎬  
> Native support for Vavoo, DaddyLive HD, and all streaming services  
> Compatible with Stremio addons when used as a MediaFlow Proxy  
> Integrated web interface and zero configuration  

---

## 📚 Contents

- [✨ Key Features](#-key-features)
- [💾 Quick Setup](#-quick-setup)
- [☁️ Cloud Deploy](#%EF%B8%8F-cloud-deploy)
- [💻 Local Installation](#-local-installation)
- [⚙️ Proxy Configuration](#%EF%B8%8F-proxy-configuration)
- [🧰 Usage](#-usage)
- [🎯 Practical Examples](#-practical-examples)
- [📖 Architecture](#-architecture)

---

## ✨ Key Features

| 🎯 **Universal Proxy** | 🔐 **Specialized Extractors** | ⚡ **Performance** |
|------------------------|------------------------|-------------------|
| HLS, M3U8, MPD, DLHD streams, VIXSRC | Vavoo, DLHD, Sportsonline, VixSrc | Async connections and keep-alive |
| **🔓 DRM Decryption** | **🎬 MPD to HLS** | **🔑 ClearKey Support** |
| ClearKey via FFmpeg transcoding | Automatic DASH → HLS conversion | Server-side ClearKey for VLC |

| 🌐 **Multi-format** | 🔄 **Retry Logic** | 🚀 **Scalability** |
|--------------------|-------------------|------------------|
| Support for #EXTVLCOPT and #EXTHTTP | Automatic retries | Asynchronous server |

| 🛠️ **Integrated Builder** | 📱 **Web Interface** | 🔗 **Playlist Manager** |
|--------------------------|----------------------|---------------------|
| M3U playlist combination | Complete dashboard | Automatic header management |
| **📼 Integrated DVR** | **⏯️ Smart Record** | **💾 Download** |
| Record while watching | Simultaneous Start & Watch | Download your recordings |

---

## 💾 Quick Setup

### 🐳 Docker (Recommended)

**Ensure you have a `Dockerfile` and `requirements.txt` in the root of the project.**

```bash
git clone https://github.com/stremio-manager/EasyProxy.git
cd EasyProxy
docker build -t EasyProxy .
docker run -d -p 7860:7860 --name EasyProxy EasyProxy
```

### 🐍 Direct Python

```bash
git clone https://github.com/stremio-manager/EasyProxy.git
cd EasyProxy
pip install -r requirements.txt
python app.py
```

**Server available at:** `http://localhost:7860`

---

## ☁️ Cloud Deploy

### ▶️ Render

1. **Projects** → **New → Web Service** → *Public Git Repository*
2. **Repository**: `https://github.com/stremio-manager/EasyProxy`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn --bind 0.0.0.0:7860 --workers 4 --worker-class aiohttp.worker.GunicornWebWorker app:app`
5. **Deploy**

### 🤖 HuggingFace Spaces

1. Create a new **Space** (SDK: *Docker*)
2. Upload all files
3. Automatic deploy
4. **Ready!**

**Alternative:** Alternatively, you can copy the content of final `Dockerfile-hf` and put it on HuggingFace, setting `api_password` as a secret.

### 🌐 Railway / Heroku

```bash
# Railway
railway login && railway init && railway up

# Heroku
heroku create EasyProxy && git push heroku main
```

### 🚀 Koyeb
1. Create a new **Web Service** on Koyeb.
2. Select **GitHub** as the source and enter the repository URL: `https://github.com/stremio-manager/EasyProxy`
3. Select Dockerfile
4. Select CPU Eco - Free
5. Go to **Environment variables**.
6. Add the `PORT` variable with value `8000` (required by Koyeb).
7. Deploy!

### 🎯 Optimal Cloud Configuration

**The proxy works without configuration!**

Optimized for:
- ✅ **Free platforms** (HuggingFace, Render Free)
- ✅ **Limited servers** (512MB - 1GB RAM)
- ✅ **Direct streaming** without cache
- ✅ **Maximum compatibility** with all services

---

## 💻 Local Installation

### 📋 Requirements

- **Python 3.8+**
- **FFmpeg** (necessary for transcoding MPD streams)
- **aiohttp**
- **gunicorn** (optional, recommended for Linux)

> ⚠️ **Note:** If not using Docker, you must install FFmpeg manually:
> - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
> - **Linux/Debian**: `sudo apt install ffmpeg`
> - **macOS**: `brew install ffmpeg`
> - **Termux**: `pkg install ffmpeg`

### 🔧 Full Installation

```bash
# Clone repository
git clone https://github.com/stremio-manager/EasyProxy.git
cd EasyProxy

# Install dependencies
pip install -r requirements.txt

# Start 
gunicorn --bind 0.0.0.0:7860 --workers 4 --worker-class aiohttp.worker.GunicornWebWorker app:app

# Start on Windows
python app.py
```

### 🐧 Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python git ffmpeg -y
git clone https://github.com/stremio-manager/EasyProxy.git
cd EasyProxy
pkg install clang libxml2 libxslt python
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python app.py
```

### 🐳 Advanced Docker

```bash
# Custom Build
docker build -t EasyProxy .

# Run with custom configurations
docker run -d -p 7860:7860 \
  --name EasyProxy EasyProxy

# Run with volume for logs
docker run -d -p 7860:7860 \
  -v $(pwd)/logs:/app/logs \
  --name EasyProxy EasyProxy
```

---

## ⚙️ Proxy Configuration

The easiest way to configure proxies is through a `.env` file.

1.  **Create a `.env` file** in the main project folder (you can rename the `.env.example` file).
2.  **Add your proxy variables** to the `.env` file.

**Example `.env` file:**

```env
# Global proxy for all traffic
GLOBAL_PROXY=http://user:pass@myproxy.com:8080

# --- Transport Rules (TRANSPORT_ROUTES) ---
# Advanced system for proxy routing based on URL patterns.
# Format: {URL=pattern, PROXY=proxy_url, DISABLE_SSL=true}, {URL=pattern2, PROXY=proxy_url2, DISABLE_SSL=true}
# - URL: pattern to search for in the URL (e.g., vavoo.to, dlhd.dad, giokko.ru)
# - PROXY: proxy to use (leave empty for direct connection)
# - DISABLE_SSL: to disable SSL verification

TRANSPORT_ROUTES={URL=vavoo.to, PROXY=socks5://proxy1:1080, DISABLE_SSL=true}, {URL=dlhd.dad, PROXY=http://proxy2:8080, DISABLE_SSL=true}

# Password to protect the APIs
API_PASSWORD=mysecretpassword

# --- MPD Processing Mode ---
# Choose how to handle MPD/DASH streams:
# - ffmpeg: Transcoding via FFmpeg (requires FFmpeg installed, high CPU but better A/V sync)
# - legacy: Uses mpd_converter + drm_decrypter (lighter but possible compatibility issues)
MPD_MODE=legacy

# --- Log Level ---
# Set the logging verbosity level: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Default: WARNING (shows only warnings and errors for cleaner output)
# Use DEBUG for development/troubleshooting, INFO for normal operation details
LOG_LEVEL=WARNING

# --- DVR/Recording Settings ---
# Enable DVR/recording functionality (default: false)
DVR_ENABLED=false

# Directory where recordings will be saved (default: recordings)
RECORDINGS_DIR=recordings

# Maximum recording duration in seconds (default: 28800 = 8 hours)
MAX_RECORDING_DURATION=28800

# Auto-delete recordings older than X days (default: 7)
RECORDINGS_RETENTION_DAYS=7
```

Supported variables:
- `GLOBAL_PROXY`: Fallback proxy for all requests.
- `TRANSPORT_ROUTES`: Advanced system for proxy routing based on URL patterns.
- `PORT`: Port the server listens on (default: 7860).
- `API_PASSWORD`: Password to protect API access.
- `MPD_MODE`: MPD processing mode (`ffmpeg` or `legacy`). Default: `legacy`.
- `LOG_LEVEL`: used to config the log level verbosity, see env file for the different values.
- `DVR_ENABLED`: enables the DVR functionality, <ins>needs to be switched to true</ins>.
- `RECORDINGS_DIR`: directory where to save recordings.
- `MAX_RECORDING_DURATION`: max recording duration.
- `RECORDINGS_RETENTION_DAYS`: days after the recordings are deleted automatically, before deletion recordings completed can be downloaded.

**Example to change the port:**

```env
# Change the server port (default: 7860)
PORT=8080
```

---

## 📚 API Endpoints

### 🔍 Extractor API (`/extractor/video`)

This endpoint **cannot be opened directly** without parameters. It is used to extract the direct stream URL from supported services (like Vavoo, DLHD, etc.).

**Info and Help:**
If you open `/extractor` or `/extractor/video` without parameters, you will receive a JSON response with instructions and a list of supported hosts.

**How to use:**
You must add `?url=` (or `?d=`) followed by the video link you want to process.

**Practical Examples:**

1.  **Get JSON with details (Default):**
    ```
    http://your-server:7860/extractor/video?url=https://vavoo.to/channel/123
    ```
    *Returns a JSON with `destination_url`, `request_headers`, etc.*

2.  **Redirect directly to stream (Redirect):**
    Add `&redirect_stream=true`. Useful for putting the link directly into a player.
    ```
    http://your-server:7860/extractor/video?url=https://daddylive.mp/stream/stream-1.php&redirect_stream=true
    ```
    *The server will respond with a 302 redirect to the proxy URL ready for playback.*

3.  **Manually specify the host (Bypass Auto-detect):**
    If auto-detection fails, you can force the use of a specific extractor with `host=`.
    ```
    http://your-server:7860/extractor/video?host=vavoo&url=https://custom-link.com/123
    ```

4.  **Base64 URL:**
    You can pass the Base64 encoded URL in the `url` (or `d`) parameter. The server will automatically decode it.
    ```
    http://your-server:7860/extractor/video?url=aHR0cHM6Ly9leGFtcGxlLmNvbS92aWRlbw==
    ```

**Parameters:**
- `url` (or `d`): **(Required)** The original URL of the video or page. Supports plain text, URL Encoded, or **Base64 Encoded** links.
- `host`: (Optional) Forces the use of a specific extractor (e.g., `vavoo`, `dlhd`, `mixdrop`, `voe`, `streamtape`, `orion`).
- `redirect_stream`: 
  - `true`: Immediate redirect to the playable stream.
  - `false` (default): Returns data in JSON format.
- `api_password`: (Optional) API password if configured.

**Supported Services:**
Vavoo, DaddyLiveHD, Doodstream, F16px, Fastream, Filelions, Filemoon, Freeshot, LiveTV, Lulustream, Maxstream, Mixdrop, OKru, Orion, Sportsonline, Streamtape, Streamwish, Supervideo, Turbovidplay, Uqload, Vidmoly, Vidoza, VixSrc, Voe and Generic (for any M3U8 URL).

### 📺 Proxy Endpoints

These endpoints handle the actual proxying of video flows.

- **`/proxy/manifest.m3u8`**: Main endpoint for HLS. Also handles automatic conversion from DASH (MPD) to HLS.
- **`/proxy/hls/manifest.m3u8`**: Specific alias for HLS.
- **`/proxy/mpd/manifest.m3u8`**: Forces input to be treated as DASH (MPD).
- **`/proxy/stream`**: Universal proxy for static files (MP4, MKV, AVI) or progressive streams.

**Common Parameters:**
- `url` (or `d`): URL of the original stream.
- `h_<header>`: Custom headers (e.g., `h_User-Agent=VLC`).
- `clearkey`: DRM decryption keys in `KID:KEY` format (for protected MPD streams).

### 📼 DVR / Recordings

The server includes a complete recording system (DVR).

- **`/recordings`**: Web Interface to manage recordings, <ins>if set, also the webpage requested via the browser needs to have the API_PASSWORD in the query string params</ins>.
- **`/record`**: "Smart" endpoint to start recording and watching simultaneously.
  - Example: `/record?url=STREAM_URL&name=Movie` -> Starts rec and redirects to stream.
- **`/api/recordings/start` (POST)**: Starts a recording in the background.
- **`/api/recordings/{id}/stream`**: Watch a recording. For active recordings, streams in real-time without stopping the recording.
- **`/api/recordings/{id}/download`**: Download the recorded file.

### 🛠️ Utilities

- **`/builder`**: Web Interface for the Playlist Builder.
- **`/playlist`**: Endpoint to process entire remote M3U playlists.
- **`/info`**: HTML page with server status and component versions.
- **`/api/info`**: JSON API returning server status.
- **`/proxy/ip`**: Returns the server's public IP address (useful for VPN/Proxy debugging).
- **`/generate_urls`** (POST): Batch generates proxy URLs (used by the Builder).
- **`/license`**: Endpoint to handle DRM license requests (if necessary).

---

## 📚 Full API Reference

Comprehensive list of all endpoints available in the server.

### 🏠 System & Public
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/` | Main page with server status. |
| `GET` | `/info` | Detailed information page. |
| `GET` | `/builder` | Playlist Builder Web Interface. |
| `GET` | `/api/info` | Server status API (JSON). |
| `GET` | `/proxy/ip` | Returns server's public IP (useful for VPN debug). |

### 📺 Proxy & Streaming
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/proxy/manifest.m3u8` | **Main Entrypoint**. Auto-detect HLS/DASH. |
| `GET` | `/proxy/hls/manifest.m3u8` | Specific alias for HLS. |
| `GET` | `/proxy/mpd/manifest.m3u8` | Forces DASH (MPD) input with HLS conversion. |
| `GET` | `/proxy/stream` | Generic proxy for static (MP4, MKV) or progressive files. |
| `GET` | `/playlist` | Dynamic M3U playlist generator. |

### 🔍 Extractors
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/extractor/video` | Extracts direct links from supported sites (Vavoo, DLHD, etc.). Returns JSON or redirect. |

### 🔐 Keys & DRM
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/license` | Proxy for DRM licenses (ClearKey/Widevine). |
| `POST` | `/license` | Proxy for DRM licenses (POST payload support). |
| `GET` | `/key` | Proxy for standard AES-128 decryption keys. |

### 📼 DVR (Digital Video Recorder)
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/recordings` | **Web Interface** for recording management. |
| `GET` | `/record` | Starts recording and redirects to stream (Smart Mode). |
| `GET` | `/api/recordings` | List all recordings (JSON). |
| `GET` | `/api/recordings/active` | List only ongoing recordings. |
| `GET` | `/api/recordings/{id}` | Details of a single recording. |
| `POST` | `/api/recordings/start` | Starts background recording (JSON payload). |
| `POST` | `/api/recordings/{id}/stop` | Stops an active recording. |
| `GET` | `/api/recordings/{id}/stream` | Watch a recording. For active recordings, streams the growing file in real-time without stopping. |
| `GET` | `/api/recordings/{id}/download` | Download the recorded video file. |
| `DELETE` | `/api/recordings/{id}` | Delete a recording. |

---

## 🧰 Usage

Replace `<server-ip>` with your server's IP address.

### 🎯 Main Web Interface

```
http://<server-ip>:7860/
```

### 📺 Universal HLS Proxy

```
http://<server-ip>:7860/proxy/manifest.m3u8?url=<STREAM_URL>
```

**Supports:**
- **HLS (.m3u8)** - Live and VOD streaming
- **M3U playlist** - IPTV channel lists  
- **MPD (DASH)** - Adaptive streaming with automatic HLS conversion
- **MPD + ClearKey DRM** - Server-side CENC decryption (VLC compatible)
- **DLHD streams** - Dynamic streams (DaddyLiveHD)
- **VixSrc** - VOD streaming
- **Sportsonline** - Sports streaming
- **Mixdrop** - Video file hosting
- **Voe** - Video hosting
- **Streamtape** - Video hosting
- **Orion** - Video streaming
- **Freeshot/PopCDN** - CDN streaming
- **Doodstream** - Video hosting
- **F16px** - Video streaming
- **Fastream** - Video streaming
- **Filelions** - Video hosting
- **Filemoon** - Video hosting
- **LiveTV** - Live TV streaming
- **Lulustream** - Video streaming
- **Maxstream** - Video streaming
- **OKru** - Video hosting (ok.ru)
- **Streamwish** - Video streaming
- **Supervideo** - Video hosting
- **Turbovidplay** - Video streaming
- **Uqload** - Video hosting
- **Vidmoly** - Video streaming
- **Vidoza** - Video hosting

**Examples:**
```bash
# Generic HLS stream
http://server:7860/proxy/manifest.m3u8?url=https://example.com/stream.m3u8

# MPD with ClearKey DRM (server-side decryption)
http://server:7860/proxy/manifest.m3u8?url=https://cdn.com/stream.mpd&clearkey=KID:KEY

# IPTV Playlist
http://server:7860/playlist?url=https://iptv-provider.com/playlist.m3u

# Stream with custom headers
http://server:7860/proxy/manifest.m3u8?url=https://stream.com/video.m3u8&h_user-agent=VLC&h_referer=https://site.com
```
### 📼 DVR (Digital Video Recorder)

Remember that to use the DVR functionality you need to enable it via the env var.
If the proxy is secured with a password it needs to be sent with the query string in the url: `/recordings?api_password=<password>`.

```
# Web Interface for recording management
http://<server-ip>:7860/recordings
```

### 🔍 Automatic Vavoo Extraction

**Automatically resolves:**
- vavoo.to links into direct streams
- Automatic API authentication
- Optimized headers for streaming

### 📡 Automatic DaddyLive HD Resolution

**Features:**
- DaddyLive HD link resolution
- Automatic restriction bypass
- Stream quality optimization

### ⚽ Automatic Sportsonline/Sportzonline resolution

**Features:**
- Resolution of links from `sportsonline.*` and `sportzonline.*`
- Automatic extraction from iframe
- Support for Javascript decoding (P.A.C.K.E.R.)

### 🔗 Playlist Builder

```
http://<server-ip>:7860/builder
```

**Complete interface for:**
- ✅ Combining multiple playlists
- ✅ Automatic Vavoo and DLHD management
- ✅ #EXTVLCOPT and #EXTHTTP support  
- ✅ Automatic #KODIPROP ClearKey extraction
- ✅ Automatic proxy for all streams
- ✅ Compatibility with VLC, Kodi, IPTV players

### 🔑 Custom Headers

Add headers with the `h_` prefix:

```
http://server:7860/proxy/manifest.m3u8?url=STREAM_URL&h_user-agent=CustomUA&h_referer=https://site.com&h_authorization=Bearer token123
```

**Supported Headers:**
- `h_user-agent` - Custom User Agent
- `h_referer` - Reference site  
- `h_authorization` - Authorization token
- `h_origin` - Origin domain
- `h_*` - Any custom header

---

## 📖 Architecture

### 🔄 Processing Flow

1. **Stream Request** → Universal proxy endpoint
2. **Service Detection** → Auto-detect Vavoo/DLHD/Generic
3. **URL Extraction** → Real link resolution
4. **Proxy Stream** → Forward with optimized headers
5. **Client Response** → Direct compatible stream

### ⚡ Asynchronous System

- **aiohttp** - Non-blocking HTTP client
- **Connection pooling** - Reuse of connections
- **Automatic retry** - Intelligent error management

### 🔐 Authentication Management

- **Vavoo** - Automatic signature system
- **DaddyLive** - Specialized headers  
- **Generic** - Standard Authorization support

---

## 🎯 Practical Examples

### 📱 IPTV Player

Configure your player with:
```
http://your-server:7860/proxy/manifest.m3u8?url=STREAM_URL
```

### 🎬 VLC Media Player

```bash
vlc "http://your-server:7860/proxy/manifest.m3u8?url=https://example.com/stream.m3u8"
```

### 📺 Kodi

Add as a source:
```
http://your-server:7860/proxy/manifest.m3u8?url=PLAYLIST_URL
```

### 🌐 Web Browser

Open directly in the browser:
```
http://your-server:7860/proxy/manifest.m3u8?url=https://stream.example.com/live.m3u8
```

---

### 🔧 Docker Management

```bash
# Real-time logs
docker logs -f EasyProxy

# Restart container
docker restart EasyProxy

# Stop/Start
docker stop EasyProxy
docker start EasyProxy

# Complete removal
docker rm -f EasyProxy
```

---

## 🚀 Performance

### 📊 Typical Benchmarks

| **Metric** | **Value** | **Description** |
|------------|------------|-----------------|
| **Latency** | <50ms | Minimal proxy overhead |
| **Throughput** | Unlimited | Limited by available bandwidth |
| **Connections** | 1000+ | Supported simultaneous connections |
| **Memory** | 50-200MB | Typical usage |

### ⚡ Optimizations

- **Connection Pooling** - Reusing HTTP connections
- **Async I/O** - Non-blocking request handling
- **Keep-Alive** - Persistent connections
- **DNS Caching** - Domain resolution cache

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a branch for changes (`git checkout -b feature/AmazingFeature`)
3. **Commit** the changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### 🐛 Bug Reporting

To report bugs, open an issue including:
- Proxy version
- Operating system
- Test URL causing the problem
- Full error log

### 💡 Feature Requests

For new features, open an issue describing:
- Desired functionality
- Specific use case
- Priority (low/medium/high)

---

## 📄 License

This project is distributed under the MIT license. See the `LICENSE` file for more details.

---

<div align="center">

**⭐ If this project is helpful to you, leave a star! ⭐**

> 🎉 **Enjoy Your Streaming!**  
> Access your favorite content anywhere, without restrictions, with complete control and optimized performance.

</div>
