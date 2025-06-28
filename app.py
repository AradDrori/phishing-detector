from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan_email():
    data = request.get_json()

    if not data or "subject" not in data or "body" not in data:
        return jsonify({"error": "Missing 'subject' or 'body' in request"}), 400

    subject = data["subject"]
    body = data["body"]

    # לוגיקה פשוטה לזיהוי פישינג לדוגמה
    suspicious_keywords = ["click here", "reset your password", "verify your account", "bank account", "urgent"]
    full_text = f"{subject} {body}".lower()

    is_phishing = any(keyword in full_text for keyword in suspicious_keywords)

    return jsonify({
        "phishing": is_phishing,
        "reason": "Suspicious keywords found" if is_phishing else "No suspicious content detected"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
