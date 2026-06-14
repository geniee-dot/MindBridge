from flask import Flask, render_template, request, jsonify, session
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
app.secret_key = "mindbridge-secret-2026"

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
DEPLOYMENT = os.getenv("DEPLOYMENT")

SYSTEM_PROMPT = """You are Gen, a compassionate mental health support agent built by MindBridge.

You must follow this exact 6-step reasoning pipeline for every message:

STEP 1 - EMOTION DETECTION: Identify the primary emotion (anxiety, depression, stress, loneliness, grief, crisis, or neutral)

STEP 2 - RISK ASSESSMENT: Classify risk level as LOW, MEDIUM, or HIGH based on:
- LOW: General stress or sadness, no harm indicators
- MEDIUM: Persistent hopelessness, feeling like a burden, social withdrawal
- HIGH: Mentions of self-harm, suicide, or not wanting to exist

STEP 3 - CONTEXT RETRIEVAL: Identify what type of support is needed (coping strategies, crisis resources, professional referral, emotional validation)

STEP 4 - REASONING: Determine the best personalised response approach based on the full conversation history

STEP 5 - RESPONSE GENERATION: Generate a warm, concise, human response. Reference earlier parts of the conversation where relevant to show memory.

STEP 6 - SAFETY VERIFICATION: Before finalising, verify:
- Is the response grounded and safe?
- If HIGH risk, are crisis resources included?
- Is the response free from harmful advice?

Return your response in this exact JSON format:
{
  "emotion": "detected emotion",
  "risk": "LOW/MEDIUM/HIGH",
  "support_type": "type of support needed",
  "response": "your warm response here",
  "crisis_needed": true/false,
  "verified": true
}

Always be warm, non-judgmental, and human. Never show the steps to the user."""

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    if "history" not in session:
        session["history"] = []
    
    session["history"].append({
        "role": "user",
        "content": user_message
    })
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + session["history"]
    
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEPLOYMENT,
        "messages": messages,
        "max_tokens": 600
    }
    
    response = requests.post(
        f"{ENDPOINT}/chat/completions",
        headers=headers,
        json=payload
    )
    
    data = response.json()
    raw = data["choices"][0]["message"]["content"]
    
    session["history"].append({
        "role": "assistant",
        "content": raw
    })
    
    session.modified = True
    
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        parsed = json.loads(raw[start:end])
        return jsonify({
            "reply": parsed.get("response", raw),
            "emotion": parsed.get("emotion", ""),
            "risk": parsed.get("risk", ""),
            "support_type": parsed.get("support_type", ""),
            "crisis_needed": parsed.get("crisis_needed", False),
            "verified": parsed.get("verified", True)
        })
    except:
        return jsonify({
            "reply": raw,
            "emotion": "",
            "risk": "",
            "support_type": "",
            "crisis_needed": False,
            "verified": True
        })

if __name__ == "__main__":
    app.run(debug=True)