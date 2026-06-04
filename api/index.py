"""
JOINNEX SOLUTIONS - Flask Backend (Vercel Serverless)
"""

from flask import Flask, send_from_directory, request, jsonify
import os
import json
from datetime import datetime

# Vercel: index.html sits in the project root, one level above /api
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    static_folder=None,
    template_folder=None,
)

# Vercel exposes this as the WSGI handler
# (the variable MUST be named `app` for @vercel/python to pick it up)

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/quote", methods=["POST"])
def submit_quote():
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

    # ⚠️ IMPORTANT: Vercel's filesystem is READ-ONLY (except /tmp, which is ephemeral).
    # For production, send leads to email / database / webhook. See notes below.
    # For now, we just log to Vercel's function logs and return success.
    print("NEW LEAD:", json.dumps(record))

    return jsonify({
        "status": "success",
        "message": "Thank you. A JOINNEX strategist will reach out within one business day."
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "joinnex-solutions"}), 200


@app.errorhandler(404)
def not_found(_):
    return jsonify({"status": "error", "message": "Not found"}), 404


# Vercel runs `app` as a WSGI handler — no app.run() needed here.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
