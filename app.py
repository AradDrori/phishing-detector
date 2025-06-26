import os
from flask import Flask, request, jsonify
from phishing_detector import phishing_classifier

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan():
    email = request.get_json()
    if not email:
        return jsonify({"error": "No email data provided"}), 400

    result = phishing_classifier(email)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
