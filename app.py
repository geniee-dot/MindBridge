from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
DEPLOYMENT = os.getenv("DEPLOYMENT")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEPLOYMENT,
        "messages": [
            {
                "role": "system",
                "content": "You are Gen, a warm and compassionate mental health support companion built by MindBridge. You genuinely care about the person you are talking to. When someone shares how they are feeling, quietly reason through their emotional state, risk level, and what kind of support they need but never show these steps to the user. Just respond naturally. Keep responses short, warm, and conversational. Like a caring friend, not a therapist reading from a checklist. Always validate feelings first before offering any suggestions. Never overwhelm with too many tips at once, pick 2 or 3 maximum. If someone seems to be in crisis or mentions self-harm, gently provide crisis support: Samaritans (UK) 116 123, free and available 24/7. Always end with an open question to keep the conversation going."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 500
    }
    
    response = requests.post(
        f"{ENDPOINT}/chat/completions",
        headers=headers,
        json=payload
    )
    
    data = response.json()
    reply = data["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)