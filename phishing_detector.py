import re
from urllib.parse import urlparse

# רשימת דומיינים שאנחנו כן סומכים עליהם
TRUSTED_DOMAINS = {"gmail.com", "outlook.com", "yahoo.com", "icloud.com"}

# שלב 1 – חילוץ מרכיבי המייל
def extract_email_components(email):
    subject = email.get("subject", "")
    body = email.get("body", "")
    sender = email.get("from", "")
    # נשלוף לינקים מתוך הגוף
    links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
    return {
        "subject": subject,
        "body": body,
        "sender": sender,
        "links": links
    }

# שלב 2 – הפעלת חוקים פשוטים
def run_heuristics(components):
    reasons = []
    confidence = 0.0

    # בדיקת דומיין של השולח
    sender_domain = components["sender"].split("@")[-1]
    if sender_domain not in TRUSTED_DOMAINS:
        reasons.append("השולח מדומיין לא אמין")
        confidence += 0.3

    # בדיקת שפה דחופה בגוף ההודעה
    urgent_words = ["urgent", "immediately", "verify", "alert", "asap"]
    if any(word in components["body"].lower() for word in urgent_words):
        reasons.append("נמצאו מילים שמפעילות לחץ")
        confidence += 0.2

    # בדיקת התאמה בין דומיין השולח לדומיין הקישורים
    for link in components["links"]:
        domain = urlparse(link).netloc
        if domain and domain.split(".")[-2:] != sender_domain.split(".")[-2:]:
            reasons.append(f"קישור לדומיין זר: {domain}")
            confidence += 0.2
            break

    # סימנים חשודים בלינק
    if any("@" in link or "-" in urlparse(link).netloc for link in components["links"]):
        reasons.append("קישור עם תווים חשודים")
        confidence += 0.2

    # החלטת סיווג
    if confidence >= 0.7:
        classification = "Phishing"
    elif confidence >= 0.4:
        classification = "Suspicious"
    else:
        classification = "Safe"

    return {
        "classification": classification,
        "confidence": round(confidence, 2),
        "reasons": reasons
    }

# פונקציה ראשית שתפעיל הכל
def phishing_classifier(email):
    components = extract_email_components(email)
    return run_heuristics(components)
if __name__ == "__main__":
    test_email = {
        "subject": "Verify your account now!",
        "body": "Please click this link immediately: http://verify-now-danger.com",
        "from": "support@weirdsite.com"
    }

    result = phishing_classifier(test_email)
    print(result)

