# 🛡️ SecureScan

> A modern file security scanner built with Flask that analyzes files using VirusTotal and heuristic detection to provide fast, privacy-friendly threat assessments.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 🔍 Scan files using **VirusTotal** (70+ antivirus engines)
- 🛡️ Intelligent heuristic-based threat detection
- 🔒 Secure SHA-256 hash-based scanning (no permanent file storage)
- 📜 Scan history powered by SQLite
- ⚡ Responsive Flask web interface
- 🌐 Ready for deployment on Render or Heroku
- 🔄 Graceful fallback when VirusTotal API is unavailable

---

## 🏗️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| API | VirusTotal API |
| Deployment | Gunicorn, Render |

---

## 📂 Project Structure

```
SecureScan
├── src/
├── templates/
├── app.py
├── requirements.txt
├── .env.example
├── render.yaml
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/avartan007/SecureScan.git

cd SecureScan
```

### Create a virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

macOS/Linux

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Copy the environment template.

```bash
cp .env.example .env
```

Add your VirusTotal API key.

```
VT_API_KEY=YOUR_API_KEY
```

You can obtain a free API key from:

https://www.virustotal.com/

---

## ▶️ Run the Application

```bash
python app.py
```

Open your browser at

```
http://localhost:5000
```

---

## 🔍 How It Works

1. Upload a file.
2. Generate a SHA-256 hash.
3. Query the VirusTotal API.
4. Perform heuristic analysis.
5. Display a color-coded security verdict.
6. Store scan history locally.

---

## 📊 Security Verdict

| Status | Meaning |
|---------|----------|
| 🟢 Safe | No threats detected |
| 🟡 Suspicious | Requires further inspection |
| 🔴 Malicious | Detected by multiple antivirus engines |

---

## 📚 What I Learned

This project helped me gain practical experience with:

- REST API integration
- Secure file handling
- Hash-based malware detection
- Flask application architecture
- SQLite database design
- Environment variable management
- Error handling and graceful degradation
- Deploying Python web applications

---

## 🔮 Future Improvements

- Docker support
- Batch file scanning
- User authentication
- Threat analytics dashboard
- Redis caching
- REST API
- Dark/Light theme
- Scan report export

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Avartan Athlay**

- GitHub: https://github.com/avartan007
- LinkedIn: *(Add your LinkedIn)*
