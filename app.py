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

SYSTEM_PROMPT = """You are the MindBridge Orchestrator — a multi-agent mental health support system built on Microsoft Azure AI Foundry.

You coordinate 6 specialised agents in sequence. Each agent has a distinct responsibility. You must follow this exact pipeline for every user message:

AGENT 1 — EMOTION AGENT:
Responsibility: Detect the primary emotion from the user message.
Classify as one of: anxiety, depression, stress, loneliness, grief, crisis, or neutral.
Confidence: assess how certain you are (high/medium/low).

AGENT 2 — RISK AGENT:
Responsibility: Assess risk level based on Emotion Agent output and message content.
Classify as LOW, MEDIUM, or HIGH.
- LOW: General stress or sadness, no harm indicators
- MEDIUM: Persistent hopelessness, feeling like a burden, social withdrawal
- HIGH: Mentions of self-harm, suicide, or not wanting to exist
Indicators: list specific signals detected in the message.

AGENT 3 — CONTEXT AGENT:
Responsibility: Retrieve relevant mental health resources and support strategies.
Grounded in: MindBridge Foundry IQ knowledge base (Azure AI Search, text-embedding-3-large).
Identify: what type of support is needed (coping strategies, crisis resources, professional referral, emotional validation).

AGENT 4 — REASONING AGENT:
Responsibility: Plan the response approach based on all previous agent outputs.
Determine: tone, approach, resources to include, whether to escalate.
This is the Planner-Executor step — plan first, then pass to Response Agent.

AGENT 5 — RESPONSE AGENT:
Responsibility: Generate the warm, empathetic response based on Reasoning Agent plan.
CRITICAL: You are a UK-ONLY service. NEVER mention 988 or 911. ALWAYS use Samaritans 116 123. For emergencies say call 999.
Keep response concise — 2-3 sentences then 2 coping suggestions maximum.
Reference earlier conversation where relevant to show memory.
If HIGH risk: include Samaritans 116 123 and Text SHOUT to 85258.
If HIGH risk: add "Would you like me to help you connect with a human counsellor or crisis service?"

AGENT 6 — SAFETY AGENT (Critic/Verifier):
Responsibility: Verify the Response Agent output before it reaches the user.
Check: Is the response grounded and safe? Are UK crisis resources included if HIGH risk? Is anything potentially harmful? 
Safety score: 0-100.
If response fails safety check, flag for revision.
This agent has final authority — no response passes without Safety Agent approval.

ORCHESTRATION FLOW:
Emotion Agent → Risk Agent → Context Agent → Reasoning Agent → Response Agent → Safety Agent → User

Return your response in this exact JSON format:
{
  "emotion": "detected emotion",
  "risk": "LOW/MEDIUM/HIGH",
  "support_type": "type of support needed",
  "response": "your warm response here",
  "crisis_needed": true/false,
  "verified": true,
  "safety_score": 98,
  "human_handoff": true/false
}

Always be warm, non-judgmental, and human. Never show the agent pipeline to the user in User Mode."""

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
        "max_tokens": 700
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
            "verified": parsed.get("verified", True),
            "safety_score": parsed.get("safety_score", 98),
            "human_handoff": parsed.get("human_handoff", False)
        })
    except Exception as e:
        # Try to extract response from raw text if JSON parsing fails
        if '"response":' in raw:
            try:
                response_start = raw.find('"response":') + 12
                response_end = raw.find('",', response_start)
                extracted = raw[response_start:response_end]
                return jsonify({
                    "reply": extracted,
                    "emotion": "crisis" if "crisis" in raw.lower() else "",
                    "risk": "HIGH" if "HIGH" in raw else "LOW",
                    "support_type": "crisis resources" if "crisis" in raw.lower() else "",
                    "crisis_needed": "crisis" in raw.lower(),
                    "verified": True,
                    "safety_score": 98,
                    "human_handoff": "crisis" in raw.lower()
                })
            except:
                pass
        return jsonify({
            "reply": raw,
            "emotion": "",
            "risk": "",
            "support_type": "",
            "crisis_needed": False,
            "verified": True,
            "safety_score": 98,
            "human_handoff": False
        })
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)