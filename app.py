#!/usr/bin/env python3
"""Flask web application for file security scanning."""

import os
import hashlib
import tempfile
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from src.scanner import FileScanner
from src.database import ThreatDatabase
from src.router import FileRouter

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB limit

# Initialize components
api_key = os.getenv("VT_API_KEY")
scanner = FileScanner(api_key=api_key)
db = ThreatDatabase()
router = FileRouter()

# File validation constants
MAX_FILE_SIZE = 32 * 1024 * 1024  # 32 MB
DANGEROUS_EXTENSIONS = {
    '.exe', '.scr', '.bat', '.cmd', '.com', '.pif', '.vbs', '.js',
    '.jar', '.zip', '.rar', '.7z', '.iso', '.img', '.dmg', '.msi',
    '.dll', '.sys', '.drv', '.ocx', '.cab', '.msp', '.ps1'
}
SAFE_EXTENSIONS = {
    '.pdf', '.txt', '.doc', '.docx', '.xlsx', '.xls', '.pptx', '.ppt',
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.mp3', '.mp4'
}


def format_bytes(bytes_val):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} GB"


def get_risk_color(risk_level):
    """Get CSS color for risk level."""
    colors = {
        "CLEAN": "#27ae60",
        "SUSPICIOUS": "#f39c12",
        "MALICIOUS": "#e74c3c",
        "UNKNOWN": "#95a5a6"
    }
    return colors.get(risk_level, "#95a5a6")


def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def classify_risk_by_extension(extension):
    """Pre-classify risk based on file extension."""
    ext = extension.lower()
    if ext in DANGEROUS_EXTENSIONS:
        return "SUSPICIOUS"
    elif ext in SAFE_EXTENSIONS:
        return "CLEAN"
    return "UNKNOWN"


# Routes
@app.route("/")
def home():
    """Serve the home/hero page."""
    return render_template("home.html")


@app.route("/scanner")
def scanner_page():
    """Serve the file scanner page."""
    return render_template("scanner.html", has_api_key=bool(api_key))


@app.route("/features")
def features():
    """Serve the features/about page."""
    return render_template("features.html")


@app.route("/scan", methods=["POST"])
def scan():
    """Handle file upload and scan with multi-stage pipeline."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        # STAGE 1: Validate file size
        try:
            file_size = os.path.getsize(tmp_path)
            if file_size > MAX_FILE_SIZE:
                return jsonify({
                    "error": f"File exceeds 32 MB limit ({format_bytes(file_size)})"
                }), 400
        except Exception as e:
            return jsonify({"error": f"File size validation failed: {str(e)}"}), 400

        # STAGE 2: Compute hash and validate type
        try:
            file_hash = calculate_file_hash(tmp_path)
            _, file_ext = os.path.splitext(file.filename)
            extension_risk = classify_risk_by_extension(file_ext)
        except Exception as e:
            return jsonify({"error": f"File processing failed: {str(e)}"}), 400

        # STAGE 3 & 4: Scan the file
        result = scanner.analyze_file(tmp_path)
        
        # Ensure hash is populated
        result["hash"] = file_hash
        result["filename"] = file.filename
        result["size_bytes"] = file_size
        
        # Add size formatting
        result["size_formatted"] = format_bytes(file_size)

        # Add color for frontend
        result["color"] = get_risk_color(result["risk_level"])

        # LOGGING STAGE: Store in database for audit trail
        try:
            db.add_file(
                file_hash,
                file.filename,
                file_size,
                result["risk_level"],
                result.get("source", "Web Upload"),
                result.get("reason", "No specific threat detected")
            )
        except Exception as log_err:
            app.logger.warning(f"Database logging failed: {str(log_err)}")
        
        # Clean up temp file
        try:
            os.remove(tmp_path)
        except:
            pass

        return jsonify(result)

    except Exception as e:
        app.logger.error(f"Scan error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "api_key_configured": bool(api_key)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_ENV") == "development")
