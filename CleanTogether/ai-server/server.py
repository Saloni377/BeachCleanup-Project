from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load FAQ + eco tips
with open("cleantogether_faq.json", "r") as f:
    FAQ_DATA = json.load(f)

def find_answer(user_message):
    user_msg_lower = user_message.lower()
    for faq in FAQ_DATA:
        # Check if any keyword is in user message
        if "keywords" in faq:
            if any(kw.lower() in user_msg_lower for kw in faq["keywords"]):
                return faq["answer"]

        # Fallback: check full question match
        question_words = faq['question'].lower().split()
        if all(word in user_msg_lower for word in question_words):
            return faq["answer"]

    return "🌿 I'm sorry, I only provide information about CleanTogether and eco-friendly tips."


@app.route("/")
def home():
    return "✅ CleanTogether AI Chatbot Server Running!"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    bot_reply = find_answer(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
