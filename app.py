@app.route("/scan", methods=["POST", "GET"])
def scan_email():
    if request.method == "GET":
        return "OK", 200  # עונה ל-Render כדי שידע שהשירות פעיל

    data = request.get_json()
    if not data or "subject" not in data or "body" not in data:
        return jsonify({"error": "Missing 'subject' or 'body' in request"}), 400

    subject = data["subject"]
    body = data["body"]

    suspicious_keywords = ["click here", "reset your password", "verify your account", "bank account", "urgent"]
    full_text = f"{subject} {body}".lower()
    is_phishing = any(keyword in full_text for keyword in suspicious_keywords)

    return jsonify({
        "phishing": is_phishing,
        "reason": "Suspicious keywords found" if is_phishing else "No suspicious content detected"
    })
