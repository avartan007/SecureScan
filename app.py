#!/usr/bin/env python3
"""Flask web application for file security scanning."""

import os
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
    """Handle file upload and scan."""
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

        # Scan the file
        result = scanner.analyze_file(tmp_path)

        # Add size formatting
        if result.get("size_bytes"):
            result["size_formatted"] = format_bytes(result["size_bytes"])

        # Add color for frontend
        result["color"] = get_risk_color(result["risk_level"])

        # Store in database
        if result.get("hash"):
            db.add_file(
                result["hash"],
                result["filename"],
                result.get("size_bytes", 0),
                result["risk_level"],
                result.get("source", "Web Upload")
            )

        # Clean up temp file
        try:
            os.remove(tmp_path)
        except:
            pass

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "api_key_configured": bool(api_key)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_ENV") == "development")
