# 🛡️ File Security Scanner

A simple, honest file security scanner. Upload a file → get a verdict: **CLEAN**, **SUSPICIOUS**, **MALICIOUS**, or **UNKNOWN**.

Powered by VirusTotal's collective security intelligence (70+ antivirus vendors) with a smart fallback to extension-based risk assessment.

---

## What It Does

1. **You upload a file** (drag & drop or click)
2. **We hash it** (SHA-256 — creates a unique fingerprint)
3. **We check VirusTotal** (if API key configured) — "Have 70+ antivirus vendors seen this file before?"
4. **You get instant feedback** — Color-coded result with reasoning

**No files are stored on the server.** File deleted after scanning. Only the hash gets analyzed.

---

## Features

| Feature | Details |
|---------|---------|
| **Simple Web UI** | Mobile-friendly, single-page app. No dependencies or heavy frameworks. |
| **Two-tier scanning** | VirusTotal API (primary) + Extension-based fallback (always available) |
| **Works without API key** | Uses extension-based classification if you don't have VirusTotal key |
| **Instant results** | Shows hash, file size, risk reason, detection count (if available) |
| **File history** | SQLite database tracks all scanned files by hash |
| **No storage** | Files are deleted immediately — no upload vault |
| **Production-ready** | Runs on Render free tier, Heroku, or your own server |

---

## Quick Start

### Local Setup (2 minutes)

```bash
# Clone repo
git clone https://github.com/yourusername/file-security-scanner.git
cd file-security-scanner

# Create venv & install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure (optional)
cp .env.example .env
# Add your VirusTotal API key (get free one at virustotal.com)

# Run
python app.py
# Open http://localhost:5000
```

### Deploy to Render (3 clicks)

1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Create Web Service → Connect GitHub repo
4. Add env var: `VT_API_KEY=your_key` (optional)
5. Deploy

Done. Live in 2 minutes.

---

## How to Get a Free VirusTotal API Key

1. Visit https://www.virustotal.com/gui/home/upload
2. Sign up (free account)
3. Go to Settings → API
4. Copy your API key
5. Add it to `.env`: `VT_API_KEY=your_key_here`

Without an API key? The app still works — it just uses file extension analysis instead.

---

## Project Structure

```
file-security-scanner/
├── app.py                    # Flask web app
├── Procfile                  # Deploy instruction for Render/Heroku
├── render.yaml               # Render-specific config
├── requirements.txt          # Python dependencies
├── .env.example              # Template for environment variables
├── README.md                 # This file
├── LICENSE
└── src/
    ├── __init__.py
    ├── scanner.py            # File scanning logic
    ├── database.py           # SQLite threat database
    └── router.py             # File organization
└── templates/
    └── index.html            # Web UI
```

---

## Tech Stack

- **Backend**: Flask (Python)
- **WSGI Server**: Gunicorn (production)
- **Database**: SQLite
- **API**: VirusTotal v3
- **Frontend**: Vanilla HTML/CSS/JS (no frameworks)

---

## Security & Privacy

### What this app does:
✅ Hashes files with SHA-256  
✅ Checks hashes against VirusTotal (70+ AV vendors)  
✅ Detects suspicious file extensions  
✅ Maintains local scan history  
✅ Works completely offline (no API key required)  

### What it doesn't do:
❌ Store files on server  
❌ Read file contents  
❌ Detect zero-day vulnerabilities  
❌ Replace an antivirus on your computer  

### Privacy:
- Files are **never stored**
- Files are **deleted immediately** after scanning
- Only the **file hash** is sent to VirusTotal (not the file)
- Your API key stays in `.env` (never committed to git)

---

## Configuration

Edit `.env` (copy from `.env.example`):

```bash
# Optional: Your VirusTotal API key (free tier available)
VT_API_KEY=

# Don't change these (production defaults)
FLASK_ENV=production
```

If you don't add an API key, the app works fine with extension-based scanning.

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve the web UI |
| `/scan` | POST | Upload and scan a file |
| `/health` | GET | Health check (returns `{"status": "ok"}`) |

### Example `/scan` request:

```bash
curl -X POST -F "file=@myfile.exe" http://localhost:5000/scan
```

Response:
```json
{
  "filename": "myfile.exe",
  "hash": "abc123...",
  "size_bytes": 524288,
  "risk_level": "SUSPICIOUS",
  "reason": "Executable file type",
  "source": "Extension-based",
  "status": "SCANNED"
}
```

---

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `VT_API_KEY` | No | Empty | VirusTotal API key (enables cloud scanning) |
| `FLASK_ENV` | No | `production` | Flask environment mode |
| `PORT` | No | `5000` | Port to listen on (auto-set by Render) |

---

## Performance Notes

- **File size limit**: 32 MB
- **Response time**: <500ms (local scanning), 1-2s (VirusTotal API)
- **VirusTotal rate limit**: 4 requests/minute (free tier)
- **Database**: Single SQLite file, suitable for <100k scans

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'flask'"**  
→ Run `pip install -r requirements.txt`

**"VirusTotal API errors"**  
→ Check your API key in `.env`  
→ Verify you're not exceeding 4 requests/minute

**"File upload fails"**  
→ Check file size (<32 MB)  
→ Ensure `/tmp` has space for temp files

**App works locally but fails on Render**  
→ Check Render logs: Settings → Logs  
→ Verify `VT_API_KEY` env var is set (if using)

---

## Development

Want to improve this? Here's how:

```bash
# Install dev dependencies (if needed)
pip install -r requirements.txt

# Make changes
# Test locally: python app.py
# Push to GitHub
# Render auto-redeploys
```

---

## License

MIT — Use it, modify it, distribute it. No attribution required.

---

## Links

- **VirusTotal API docs**: https://developers.virustotal.com/reference/files-get
- **Flask docs**: https://flask.palletsprojects.com/
- **Render deployment**: https://render.com/docs/web-services

---

**Built by someone curious about security. Zero marketing BS, just honest code.**
2. **Organize** - Sort results into `files/approved` & `files/suspicious`
3. **Results** - View scan summary and file details
4. **Exit** - Quit cleanly

### As a Python Library

```python
from src import FileScanner

# Create scanner instance
scanner = FileScanner(api_key="your_key", auto_extract_archives=True)

# Scan directory
results = scanner.scan_directory("./files", recursive=True)

# Save results to JSON
scanner.save_results("scan_results.json")

# Get results
summary = scanner.get_results()
print(f"Scanned {len(summary)} files")
```

### Advanced: Custom Analysis

```python
from src import FileScanner, FileRouter, TrustIntelligenceGraph

scanner = FileScanner()
router = FileRouter()
intel = TrustIntelligenceGraph()

# Analyze individual file
result = scanner.analyze_file("./file.exe")
print(f"Risk Level: {result['risk_level']}")

# Track file in database
intel.record_file(result['hash'], "file.exe", 
                 source="Manual_Scan",
                 risk_level=result['risk_level'])

intel.close()
```

---

## 📊 Results Classification

| Status | Icon | Meaning |
|--------|------|---------|
| **CLEAN** | ✅ | No threats detected |
| **SUSPICIOUS** | 🟠 | Potential malware |
| **MALICIOUS** | 🔴 | High-risk file |
| **SKIPPED** | ⏭️ | File too large (>32MB) |
| **DUPLICATE** | 🔄 | Already scanned |

---

## 📁 Project Structure

```
file-security-scanner/
├── src/
│   ├── __init__.py                 # Package exports
│   ├── main.py                     # CLI & orchestration
│   ├── file_scanner.py             # Core scanning engine
│   ├── file_router.py              # File organization
│   ├── audit_logger.py             # Audit trail logging
│   └── trust_intelligence.py       # Threat intelligence DB
│
├── books/                          # Input directory (files to scan)
├── files/
│   ├── approved/                   # Safe files
│   ├── suspicious/                 # Flagged files
│   ├── duplicates/                 # Duplicate files
│   └── quarantine/                 # High-risk files
│
├── config/
│   └── config.yaml                 # Configuration file
│
├── run.py                          # Entry point
├── setup.py                        # Package installation
├── requirements.txt                # Runtime dependencies
├── requirements-dev.txt            # Dev tools (removed)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
└── README.md                       # This file
```

---

## 🔧 How It Works

### 1️⃣ Scanning
- Walks through directory recursively
- Computes SHA-256 hash for each file
- Shows live progress: `[45%] 23/50`
- Checks file extension for risk classification

### 2️⃣ Risk Assessment
- **SUSPICIOUS**: `.exe`, `.bat`, `.cmd`, `.ps1`, `.vbs`, `.js`
- **CLEAN**: `.pdf`, `.txt`, `.jpg`, `.png`, `.zip`
- **UNKNOWN**: Everything else

### 3️⃣ Organization
- Copies safe files → `files/approved/`
- Copies risky files → `files/suspicious/`
- Maintains audit trail in `audit_trail.csv`

### 4️⃣ Intelligence
- Stores file metadata in SQLite database
- Tracks: hash, filename, source, risk_level, timestamp
- Enables duplicate detection & history

---

## ⚙️ Configuration

**Edit `config/config.yaml`:**

```yaml
virustotal:
  api_url: "https://www.virustotal.com/api/v3/"
  request_delay: 16    # Respect rate limits
  timeout: 10

scanner:
  max_file_size_mb: 32
  auto_extract_archives: true

logging:
  level: INFO
  format: "%(asctime)s - %(levelname)s - %(message)s"
```

---

## 📋 Requirements

- **Python**: 3.9 or higher
- **Dependencies**:
  - `requests>=2.31.0` - HTTP client
  - `python-dotenv>=1.0.0` - Environment variables

**Optional (for development):**
- `pytest` - Unit testing
- `flake8` - Code linting
- `black` - Code formatting

---

## 🎯 Example Workflow

```bash
# 1. Place files in ./books/
cp ~/Downloads/*.exe ./books/

# 2. Run scanner
python run.py

# 3. Select "1. Scan files recursively"
# → Scans all files, shows progress bar
# → Saves results to scan_results.json
# → Displays: Clean: 5, Suspicious: 2, Skipped: 1

# 4. Select "2. Organize files"
# → Copies safe files to files/approved/
# → Copies risky files to files/suspicious/
# → Updates trust_intelligence.db

# 5. Select "3. View results"
# → Shows scan summary & breakdown
```

---

## 📝 Output Files

After scanning, you'll have:

| File | Purpose |
|------|---------|
| `scan_results.json` | Scan results (hashes, risk levels) |
| `audit_trail.csv` | Complete action history |
| `trust_intelligence.db` | SQLite metadata database |

---

## 🔐 Security Notes

✅ **Safe to use:**
- No network calls to VirusTotal (optional)
- All processing is local
- No credentials stored in code
- `.env` file is in `.gitignore`

⚠️ **Best practices:**
- Keep your API key in `.env` (not in code)
- Review files before organizing them
- Use on authorized systems only
- Backup important files before scanning

---

## 📜 License

MIT License © 2024 Security Team

See [LICENSE](LICENSE) for details.

---

## 🤝 Support

Found a bug? Have a feature request?
- Open an issue on GitHub
- Include error message & Python version
- Describe your use case

---

<div align="center">

**Made with ❤️ for file security**

⭐ Star this repo if it helps you!

</div>

