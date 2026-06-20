"""
ARCHET SOLUTIONS - Flask Backend Server
Serves index.html directly from the root directory (no templates/static folders).
"""

from flask import Flask, send_from_directory, request, jsonify, abort
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone

EMAIL_FROM    = "Administrator.archetsolutions@gmail.com"
EMAIL_APP_PWD = "yvos uriv ovqs rxkd"


def send_confirmation_email(to_email, to_name, company):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<style>
  body{{margin:0;padding:0;background:#f1f3f4;font-family:'Google Sans',Roboto,Arial,sans-serif}}
  .wrap{{max-width:600px;margin:32px auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.08)}}
  .header{{background:#030309;padding:28px 36px;display:flex;align-items:center;gap:12px}}
  .logo-badge{{width:36px;height:36px;border-radius:10px;background:rgba(15,255,212,.12);border:1px solid rgba(15,255,212,.3);display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;color:#0FFFD4;text-align:center;line-height:36px}}
  .logo-text{{color:#fff;font-size:18px;font-weight:700;letter-spacing:-.3px}}
  .logo-sub{{color:rgba(255,255,255,.35);font-size:10px;letter-spacing:3px;text-transform:uppercase;margin-top:1px}}
  .body{{padding:36px 36px 28px}}
  .greeting{{font-size:20px;font-weight:500;color:#202124;margin-bottom:6px}}
  .intro{{font-size:14px;color:#5f6368;line-height:1.6;margin-bottom:24px}}
  .card{{background:#f8f9fa;border:1px solid #e8eaed;border-radius:8px;padding:20px 24px;margin-bottom:24px}}
  .card-title{{font-size:11px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;color:#80868b;margin-bottom:12px}}
  .card-row{{display:flex;gap:8px;margin-bottom:6px;font-size:13px}}
  .card-label{{color:#80868b;min-width:90px;flex-shrink:0}}
  .card-val{{color:#202124;font-weight:500}}
  .divider{{height:1px;background:#e8eaed;margin:20px 0}}
  .next-steps{{font-size:14px;color:#5f6368;line-height:1.7;margin-bottom:24px}}
  .next-steps strong{{color:#202124}}
  .badge{{display:inline-block;background:#e8f5e9;color:#137333;font-size:12px;font-weight:600;padding:4px 12px;border-radius:100px;margin-bottom:20px}}
  .cta-block{{text-align:center;margin:8px 0 24px}}
  .cta{{display:inline-block;background:#030309;color:#0FFFD4;font-size:14px;font-weight:600;padding:12px 28px;border-radius:8px;text-decoration:none;letter-spacing:-.1px}}
  .footer{{background:#f8f9fa;border-top:1px solid #e8eaed;padding:20px 36px;font-size:12px;color:#80868b;text-align:center;line-height:1.6}}
  .footer a{{color:#1a73e8;text-decoration:none}}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <div class="logo-badge">A</div>
    <div>
      <div class="logo-text">ARCHET</div>
      <div class="logo-sub">Solutions</div>
    </div>
  </div>
  <div class="body">
    <div class="badge">&#10003; Request Received</div>
    <div class="greeting">Hi {to_name.split()[0]},</div>
    <p class="intro">
      Thank you for reaching out to Archet Solutions. We've received your quote request for <strong>{company}</strong> and an Archet strategist will be in touch within <strong>one business day</strong> with a tailored proposal.
    </p>

    <div class="card">
      <div class="card-title">Your submission summary</div>
      <div class="card-row"><span class="card-label">Name</span><span class="card-val">{to_name}</span></div>
      <div class="card-row"><span class="card-label">Company</span><span class="card-val">{company}</span></div>
      <div class="card-row"><span class="card-label">Email</span><span class="card-val">{to_email}</span></div>
    </div>

    <div class="next-steps">
      <strong>What happens next?</strong><br/>
      Our team reviews every request personally. You'll hear from a dedicated Archet strategist who will walk you through how we can deploy the full operations stack for your locations — no templates, no guesswork.
    </div>

    <div class="divider"></div>

    <p style="font-size:13px;color:#5f6368;margin-bottom:6px">Have an urgent need? Reach us directly:</p>
    <p style="font-size:13px;color:#202124;margin-bottom:4px">&#128222; <strong>+1 (469) 993-7957</strong></p>
    <p style="font-size:13px;color:#202124;margin-bottom:20px">&#9993; <a href="mailto:Administrator.archetsolutions@gmail.com" style="color:#1a73e8;text-decoration:none">Administrator.archetsolutions@gmail.com</a></p>

    <div class="cta-block">
      <a href="https://archetsolutions.com" class="cta">Visit Archet Solutions &rarr;</a>
    </div>
  </div>
  <div class="footer">
    &copy; {datetime.now(timezone.utc).year} Archet Solutions &nbsp;&middot;&nbsp; 20727 Stone Oak Pkwy, San Antonio, TX 78258<br/>
    <span style="color:#bdc1c6">You're receiving this because you submitted a quote request at archetsolutions.com.</span>
  </div>
</div>
</body>
</html>"""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "We received your quote request — Archet Solutions"
        msg["From"]    = f"Archet Solutions <{EMAIL_FROM}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
            srv.login(EMAIL_FROM, EMAIL_APP_PWD)
            srv.sendmail(EMAIL_FROM, to_email, msg.as_string())
    except Exception as exc:
        print(f"[email] Failed to send confirmation to {to_email}: {exc}")

# Resolve the absolute path of the directory this file lives in.
# Both joinnex.py and index.html sit in this same directory.
# Go up one level from api/ to reach the repo root where index.html lives
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        "received_at": datetime.now(timezone.utc).isoformat(),
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

    send_confirmation_email(record["email"], record["full_name"], record["company"])

    return jsonify({
        "status": "success",
        "message": "Thank you. An Archet strategist will reach out within one business day."
    }), 200


# ---------------------------------------------------------------------------
# Health check (handy for uptime monitors / load balancers).
# ---------------------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "archet-solutions"}), 200


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
