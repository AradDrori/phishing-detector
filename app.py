from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    subject = data.get('subject', '')
    body = data.get('body', '')
    
    # הדמיה של בדיקה פשוטה
    is_phishing = 'click' in body.lower() or 'password' in body.lower()

    return jsonify({'phishing': is_phishing})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
