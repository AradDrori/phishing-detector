from flask import Flask, request, jsonify
import os

# מייבא את הפונקציה שכתבת בקובץ השני
from phishing_detector import phishing_classifier

app = Flask(__name__)

@app.route("/scan", methods=["POST", "GET"])
def scan_email():
    if request.method == "GET":
        return "OK", 200

    data = request.get_json()
    if not data or "subject" not in data or "body" not in data or "from" not in data:
        return jsonify({"error": "Missing 'subject', 'body', or 'from' in request"}), 400

    # מריץ את האלגוריתם המתקדם שלך
    result = phishing_classifier(data)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
