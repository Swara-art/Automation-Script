# 🗂️ File Organiser — FastAPI Automation Script
 
> A FastAPI-powered automation script that sorts any messy folder into clean, categorised subfolders with a single API call.
 
---
 
## 📋 Table of Contents
 
- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [File Categories](#-file-categories)
- [Configuration](#-configuration)
- [How It Works](#-how-it-works)
- [Demo](#-demo)
- [Logging](#-logging)
- [Error Handling](#-error-handling)
 
---
 
## 📌 Overview
 
Manually sorting files is repetitive, time-consuming, and error-prone. This project automates the entire process — point it at any folder on your machine, call the `/organiser/run` endpoint, and every file is instantly moved into the correct subfolder based on its extension.
 
Built as a **FastAPI router** (`automate.py`) that integrates cleanly into the main FastAPI application via `main.py`. File type mappings are fully configurable via `file_types.json` — no code changes needed.
 
---
 
## ✨ Features
 
- 🚀 **Single API call** organises an entire folder instantly
- 📁 **10 built-in categories** — Images, Documents, Music, Videos, Archives, Code, Executables, Fonts, Database, Ebooks
- ⚙️ **Config-driven** — add/remove extensions in `file_types.json` without touching Python code
- 🛡️ **Safe** — never overwrites files; duplicates are auto-renamed (`file_duplicate.ext`)
- ⏭️ **Smart skipping** — existing subfolders inside the target are never moved
- 📝 **Full logging** — every action logged to `organiser.log` with timestamps
- 📊 **Structured response** — JSON summary of every file moved, skipped, or errored
 
---
 
## 📂 Project Structure
 
```
AUTOMATION SCRIPT/
├── .venv/                          # Virtual environment
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app — registers the router
│   └── routes/
│       ├── __init__.py
│       ├── automate.py             # Core router + file organiser logic
│       └── file_types.json         # Extension → category config file
├── __init__.py
├── organiser.log                   # Auto-generated activity log
├── requirements.txt
└── README.md
```
 
---
 
## 🛠️ Tech Stack
 
| Tool | Purpose |
|---|---|
| **Python 3.8+** | Core language |
| **FastAPI** | API framework |
| **Uvicorn** | ASGI server to run the app |
| **pathlib** | Cross-platform path handling |
| **shutil** | Moving files between directories |
| **logging** | Writing structured logs to file |
| **json** | Loading the file types config |
 
---
 
## 🚀 Getting Started
 
### Prerequisites
 
- Python 3.8 or higher
- pip
 
### Installation
 
**1. Clone the repository**
 
```bash
git clone https://github.com/Swara-art/Automation-Script.git
cd Automation-Script
```
 
**2. Create and activate a virtual environment**
 
```bash
# Windows
uv venv
.venv\Scripts\activate
 
# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```
 
**3. Install dependencies**
 
```bash
pip install -r requirements.txt
```
 
### Running the Server
 
```bash
uvicorn app.main:app --reload
```
 
The server starts at **`http://127.0.0.1:8000`**
 
Open **`http://127.0.0.1:8000/docs`** for the interactive Swagger UI where you can test the endpoint directly.
 
---
 
## 📡 API Reference
 
### `GET /automate/run`
 
Organises all files in the specified folder into categorised subfolders.
 
#### Query Parameters
 
| Parameter | Type | Required | Description |
|---|---|---|---|
| `folder_path` | `string` | ✅ Yes | Full absolute path to the folder to organise |
 
#### Example Request
 
```
GET http://127.0.0.1:8000/organiser/run?folder_path=C:\Users\YourName\Desktop\test_folder
```
 
#### Example Response `200 OK`
 
```json
{
  "folder": "C:/Users/YourName/Desktop/test_folder",
  "moved": [
    { "file": "resume.pdf",  "moved_to": "Documents" },
    { "file": "photo.jpg",   "moved_to": "Images"    },
    { "file": "song.mp3",    "moved_to": "Music"     },
    { "file": "backup.zip",  "moved_to": "Archives"  },
    { "file": "script.py",   "moved_to": "Code"      }
  ],
  "skipped": ["existing_subfolder"],
  "errors": [],
  "summary": {
    "total_moved": 5,
    "total_skipped": 1,
    "total_errors": 0
  }
}
```
 
#### Error Responses
 
| Status | Reason |
|---|---|
| `400` | Folder path does not exist |
| `400` | Path provided is a file, not a folder |
| `500` | Unexpected internal server error |
 
---
 
## 📁 File Categories
 
| Subfolder | Extensions Covered |
|---|---|
| `Images` | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.svg` `.webp` `.tiff` `.heic` `.raw` `.cr2` `.psd` `.ai` `.eps` |
| `Documents` | `.pdf` `.docx` `.doc` `.txt` `.pptx` `.ppt` `.xlsx` `.xls` `.csv` `.md` `.rtf` `.odt` `.pages` `.key` |
| `Music` | `.mp3` `.wav` `.flac` `.aac` `.ogg` `.wma` `.m4a` `.aiff` `.midi` `.opus` `.amr` |
| `Videos` | `.mp4` `.mkv` `.mov` `.avi` `.wmv` `.flv` `.webm` `.m4v` `.mpeg` `.3gp` `.vob` |
| `Archives` | `.zip` `.tar` `.gz` `.rar` `.7z` `.bz2` `.xz` `.tgz` `.iso` `.dmg` `.cab` |
| `Code` | `.py` `.js` `.ts` `.html` `.css` `.java` `.cpp` `.c` `.cs` `.go` `.rs` `.php` `.sql` `.yaml` `.yml` `.env` `.sh` `.bat` |
| `Executables` | `.exe` `.msi` `.apk` `.app` `.deb` `.rpm` `.pkg` `.bin` |
| `Fonts` | `.ttf` `.otf` `.woff` `.woff2` `.eot` `.fon` |
| `Database` | `.db` `.sqlite` `.sqlite3` `.mdb` `.accdb` `.sql` |
| `Ebooks` | `.epub` `.mobi` `.azw` `.azw3` `.fb2` `.djvu` |
| `Others` | Anything not matched above |
 
---
 
## ⚙️ Configuration
 
All mappings live in `app/routes/file_types.json`. Edit it freely — the script reads it fresh on every request.
 
**Adding a new extension to an existing category:**
 
```json
{
  "Images": [".jpg", ".jpeg", ".png", ".your_new_ext"],
  ...
}
```
 
**Adding a brand new category:**
 
```json
{
  ...
  "3D Models": [".obj", ".fbx", ".stl", ".blend"],
  "Others": []
}
```
 
> ⚠️ **Important:** Always keep `"Others": []` at the bottom. It is the catch-all for any extension not matched by other categories.
 
---
 
## ⚙️ How It Works
 
```
GET /organiser/run?folder_path=...
          │
          ▼
  Validate path
  (Does it exist? Is it a folder?)
          │
          ▼
  Load file_types.json
          │
          ▼
  Loop through every item in folder
          │
          ├── Is it a subfolder?
          │       └── Yes → skip it, log it
          │
          ├── Get file extension (.mp3, .pdf, etc.)
          │       └── Look up category from config
          │
          ├── Create category subfolder if it doesn't exist
          │
          ├── File already exists at destination?
          │       └── Yes → rename to filename_duplicate.ext
          │
          └── Move file → log success or error
                    │
                    ▼
          Return full JSON summary
```
 
---
 
## 🎬 Demo
 
**Folder before running the script:**
 
```
test_folder/
├── resume.pdf
├── profile_photo.jpg
├── favourite_song.mp3
├── project_backup.zip
├── index.html
├── notes.txt
└── movie.mp4
```
 
**Call the endpoint:**
 
```
GET http://127.0.0.1:8000/organiser/run?folder_path=C:\Users\Swara\Desktop\test_folder
```
 
**Folder after:**
 
```
test_folder/
├── Documents/
│   ├── resume.pdf
│   └── notes.txt
├── Images/
│   └── profile_photo.jpg
├── Music/
│   └── favourite_song.mp3
├── Archives/
│   └── project_backup.zip
├── Code/
│   └── index.html
└── Videos/
    └── movie.mp4
```
 
---
 
## 📝 Logging
 
All activity is automatically written to `organiser.log` in the project root.
 
**Log format:**
```
YYYY-MM-DD HH:MM:SS | LEVEL    | message
```
 
**Sample log:**
```
2026-04-06 10:22:01 | INFO     | Received /run request — folder_path: C:\Users\Swara\Desktop\test_folder
2026-04-06 10:22:01 | INFO     | ==================================================
2026-04-06 10:22:01 | INFO     | Organising folder: C:\Users\Swara\Desktop\test_folder
2026-04-06 10:22:01 | INFO     | Moved: resume.pdf  →  Documents/
2026-04-06 10:22:01 | INFO     | Moved: profile_photo.jpg  →  Images/
2026-04-06 10:22:01 | INFO     | Moved: favourite_song.mp3  →  Music/
2026-04-06 10:22:01 | DEBUG    | Skipped (not a file): existing_subfolder
2026-04-06 10:22:01 | ERROR    | Failed to move locked_file.exe: Permission denied
2026-04-06 10:22:01 | INFO     | Done — moved: 3, skipped: 1, errors: 1
```
 
**Log levels:**
 
| Level | When used |
|---|---|
| `INFO` | File moved, job started/finished, request received |
| `DEBUG` | Subfolders skipped, internal parsing steps |
| `ERROR` | A file failed to move |
| `CRITICAL` | Folder path is invalid or unreachable |
 
---
 
## 🛡️ Error Handling
 
| Scenario | Behaviour |
|---|---|
| Folder path doesn't exist | Returns HTTP `400` with descriptive message |
| Path is a file, not a folder | Returns HTTP `400` with descriptive message |
| File already exists in destination | Auto-renamed to `filename_duplicate.ext` |
| Subfolder found inside target folder | Skipped silently, logged as DEBUG |
| File move fails (permissions/lock) | Logged as ERROR, included in `errors[]`, script continues |
 
---
 
## 👩‍💻 Author
 
**Swara Deshpande**
