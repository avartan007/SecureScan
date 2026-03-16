# 🛡️ File Security Scanner

**Upload a file. Get instant security verdict powered by 70+ antivirus vendors.**

A lightweight web application that scans files against VirusTotal's collective security intelligence and provides color-coded risk assessment. Built to understand API integration, caching strategies, and full-stack architecture.

---

## Why I Built This

I was curious about how security tools work behind the scenes. Most people just use antivirus software without realizing there's an entire ecosystem of threat intelligence sharing (VirusTotal aggregates data from 70+ security vendors).

Rather than just learning about it, I wanted to build something that actually *uses* this intelligence. The challenge wasn't just "call an API"—it was thinking about:
- **Rate limiting**: VirusTotal has 4 requests/minute. How do I handle this gracefully?
- **Fallback strategies**: What if the API key is missing or rate-limited?
- **User experience**: How do I make security feedback immediately understandable?
- **Production readiness**: Can this actually run on Heroku/Render without issues?

This project taught me that systems thinking matters more than technical flashiness.

## ✨ Features

- **Instant Scanning** — Upload any file and get a verdict in seconds
- **Two-tier Intelligence** — Primary: VirusTotal API (70+ vendors) | Fallback: Extension-based heuristics
- **No Storage** — Files are deleted immediately after scanning. Only hashes are analyzed
- **Scan History** — SQLite database tracks all scanned file hashes for reference
- **Works Offline** — Extension-based classification works without API key
- **Beautiful UI** — Responsive web interface with real-time feedback
- **Production Ready** — Configured for Heroku and Render deployment

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=flat&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=flat&logo=sqlite)
![VirusTotal API](https://img.shields.io/badge/VirusTotal-API%20v3-orange?style=flat)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI%20Server-darkgreen?style=flat)
![HTML5/CSS3](https://img.shields.io/badge/Frontend-HTML5%2FCSS3-FF6B6B?style=flat)

**Core Dependencies:**
- **Flask 3.0.0** — Web framework
- **Requests 2.31.0** — HTTP library for VirusTotal API calls
- **Gunicorn 21.2.0** — Production WSGI server
- **Python-dotenv 1.0.0** — Environment variable management

---

## 🚀 Quick Start

### Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/avartan007/file-security-scanner.git
cd file-security-scanner

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration (Optional but Recommended)

```bash
# Copy environment template
cp .env.example .env

# Add your VirusTotal API key
# Get a free API key from: https://virustotal.com/gui/home/upload
# Then edit .env and add: VT_API_KEY=your_api_key_here
```

### Running Locally

```bash
# Development mode (with auto-reload)
PORT=5000 python app.py

# Production mode
PORT=8000 gunicorn app:app
```

**Access the app:** Open `http://localhost:5000` in your browser

---

## 📖 How It Works

### Workflow

```
┌──────────────────┐
│  User uploads    │
│  a file          │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ Calculate SHA-256 hash   │
│ (unique fingerprint)     │
└────────┬─────────────────┘
         │
         ▼
    ┌────────────────────────────────┐
    │ Check VirusTotal API (if key)  │
    │ Query 70+ antivirus vendors    │
    └────────┬──────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼ (No key)    ▼ (Has key)
   Extension-   API Results
   based Check  + Heuristics
      │             │
      └──────┬──────┘
             │
             ▼
    ┌──────────────────────┐
    │ Color-coded verdict  │
    │ GREEN / ORANGE / RED │
    └──────────────────────┘
```

### API Integration Details

- **Request handling:** GET request to VirusTotal with file hash
- **Response parsing:** Extracts detection count and vendor verdicts
- **Rate limiting:** Respects VirusTotal's 4 requests/minute limit
- **Fallback logic:** If API unavailable, uses extension-based classification
- **Caching:** SQLite stores previous results to minimize API calls

---

## 💡 What I Learned Building This

### System Design
- **Layered Architecture** — Separated concerns: Flask handlers → Scanner logic → Database layer
- **Graceful Degradation** — System works even without API key or internet
- **Rate Limiting** — Understanding API constraints and working within them

### Backend Development
- **Environment Management** — Using `.env` files for secrets (never commit actual keys)
- **WSGI Servers** — Why Gunicorn is better than Flask's dev server for production
- **Database Design** — Choosing SQLite over file storage for better query capabilities
- **Error Handling** — Making failures user-friendly instead of cryptic

### API Integration
- **Hash-based Lookup** — Smarter than uploading files (privacy + speed)
- **Vendor Aggregation** — Understanding collective threat intelligence
- **JSON Parsing** — Handling nested API responses correctly

### Frontend & UX
- **Real-time Feedback** — Using fetch API for async file uploads
- **Color Coding** — Making security status immediately intuitive
- **Responsive Design** — Mobile-first approach with CSS flexbox
- **User Psychology** — Simple, clear results reduce anxiety

### DevOps Thinking
- **Containerization** — Understanding Procfile for Heroku
- **Environment Variables** — Secure credential management
- **Deployment** — Getting code running on production platforms

---

## 🎯 Deployment

### Deploy to Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku logs --tail
```

### Deploy to Render

```bash
# One-click deploy using render.yaml
# Push to GitHub, connect repo to Render
# Render auto-deploys on git push
```

**Note:** Add `VT_API_KEY` in environment variables on the hosting platform.

---

## 🔮 Future Improvements

- **Batch Scanning** — API to submit multiple files at once
- **Statistics Dashboard** — Visualize threat patterns over time
- **PostgreSQL Migration** — Scale beyond SQLite
- **Redis Caching** — Reduce API rate limiting impact
- **Docker Support** — Containerized deployment
- **RESTful API** — Programmatic file scanning
- **WebSocket Updates** — Real-time progress tracking
- **Browser Extension** — Direct integration with downloads

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Code** | ~500 LOC (app.py) + ~300 (backend/frontend) |
| **API Coverage** | 70+ antivirus vendors |
| **Response Time** | <100ms (local) / ~500ms (API) |
| **Rate Limit** | 4 requests/minute (VirusTotal free tier) |

---

## ⚖️ License

MIT — See [LICENSE](LICENSE)

---

## 💬 A Note for Recruiters

This project demonstrates:
- **Systems thinking** — Architecture that accommodates real constraints
- **User-centric design** — Making security understandable
- **Production readiness** — Code that actually runs in production
- **Continuous learning** — Reflection on what worked and what's next

Built by a final-year CS student exploring why good architecture matters.

---

**Status**: ✅ Production Ready | Updated: March 2026

