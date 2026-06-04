"""
JOINNEX SOLUTIONS - Flask Backend Server
Serves index.html directly from the root directory (no templates/static folders).
"""

from flask import Flask, send_from_directory, request, jsonify, abort
import os
import json
from datetime import datetime

# Resolve the absolute path of the directory this file lives in.
# Both joinnex.py and index.html sit in this same directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Disable Flask's default template_folder and static_folder so it does
# NOT look for a /templates or /static directory at all.
app = Flask(
    __name__,
    static_folder=None,
    template_folder=None,
)

# ---------------------------------------------------------------------------
# Route: Serve the homepage (index.html) directly from the project root.
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    """
    Safely serves index.html from BASE_DIR using send_from_directory,
    which guards against path traversal attacks.
    """
    return send_from_directory(BASE_DIR, "index.html")


# ---------------------------------------------------------------------------
# Route: Lead capture endpoint for the B2B quote form.
# ---------------------------------------------------------------------------
@app.route("/api/quote", methods=["POST"])
def submit_quote():
    """
    Accepts JSON or form-encoded data from the website's quote form.
    Persists each submission to a local leads.json file (append-only).
    """
    # Accept both JSON payloads (fetch) and standard form posts.
    payload = request.get_json(silent=True) or request.form.to_dict()

    required_fields = ["full_name", "company", "email", "brand"]
    missing = [f for f in required_fields if not payload.get(f, "").strip()]
    if missing:
        return jsonify({
            "status": "error",
            "message": f"Missing required fields: {', '.join(missing)}"
        }), 400

    record = {
        "received_at": datetime.utcnow().isoformat() + "Z",
        "full_name": payload.get("full_name", "").strip(),
        "company":   payload.get("company", "").strip(),
        "email":     payload.get("email", "").strip(),
        "phone":     payload.get("phone", "").strip(),
        "brand":     payload.get("brand", "").strip(),
        "stores":    payload.get("stores", "").strip(),
        "message":   payload.get("message", "").strip(),
    }

    leads_path = os.path.join(BASE_DIR, "leads.json")
    try:
        existing = []
        if os.path.exists(leads_path):
            with open(leads_path, "r", encoding="utf-8") as fh:
                try:
                    existing = json.load(fh)
                except json.JSONDecodeError:
                    existing = []
        existing.append(record)
        with open(leads_path, "w", encoding="utf-8") as fh:
            json.dump(existing, fh, indent=2)
    except OSError as exc:
        return jsonify({
            "status": "error",
            "message": f"Could not persist lead: {exc}"
        }), 500

    return jsonify({
        "status": "success",
        "message": "Thank you. A JOINNEX strategist will reach out within one business day."
    }), 200


# ---------------------------------------------------------------------------
# Health check (handy for uptime monitors / load balancers).
# ---------------------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "joinnex-solutions"}), 200


# ---------------------------------------------------------------------------
# Block any attempt to fetch other arbitrary files from the root directory.
# Only /, /health, and /api/quote are exposed.
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_):
    return jsonify({"status": "error", "message": "Not found"}), 404


if __name__ == "__main__":
    # debug=False is recommended for production; flip to True while developing.
    app.run(host="0.0.0.0", port=5000, debug=True)