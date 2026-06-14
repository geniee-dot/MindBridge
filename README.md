
# 🌿 MindBridge — AI Mental Health Reasoning Agent

> An AI agent that detects emotional crisis, explains its reasoning, and routes users to verified support before a situation escalates.

Built for the **Microsoft Agents League Hackathon 2026 — Track 2: Reasoning Agents**

---

## 🧠 What is MindBridge?

MindBridge is a multi-agent mental health support system built on Microsoft Azure AI Foundry. At its core is **Gen** — a compassionate orchestrator that coordinates 6 specialised agents to provide safe, grounded, and explainable emotional support to anyone in distress.

MindBridge is the only mental health reasoning agent in the hackathon. It is built by an MSc Data Science and Artificial Intelligence student whose intended PhD research focuses on privacy-preserving AI for mental health detection.

---

## 🤖 Multi-Agent Architecture

MindBridge implements a genuine multi-agent pipeline. Each agent has a distinct responsibility:

```
User Message
     ↓
Orchestrator Agent (Gen)
     ↓
┌─────────────────────────────────────────┐
│  Agent 1: Emotion Agent                 │
│  Detects primary emotion from message   │
│  Output: anxiety / depression / crisis  │
├─────────────────────────────────────────┤
│  Agent 2: Risk Agent                    │
│  Classifies risk level                  │
│  Output: LOW / MEDIUM / HIGH            │
├─────────────────────────────────────────┤
│  Agent 3: Context Agent                 │
│  Retrieves verified mental health       │
│  resources from Foundry IQ knowledge    │
│  base (Azure AI Search)                 │
├─────────────────────────────────────────┤
│  Agent 4: Reasoning Agent               │
│  Plans response approach                │
│  Pattern: Planner-Executor              │
├─────────────────────────────────────────┤
│  Agent 5: Response Agent                │
│  Generates warm empathetic response     │
│  UK crisis resources only               │
├─────────────────────────────────────────┤
│  Agent 6: Safety Agent                  │
│  Critic/Verifier pattern                │
│  Final authority — no response passes   │
│  without Safety Agent approval          │
│  Safety score: 0-100                    │
└─────────────────────────────────────────┘
     ↓
Verified Response to User
```

---

## 🎯 Reasoning Patterns Implemented

| Pattern | Implementation |
|---|---|
| Planner-Executor | Reasoning Agent plans, Response Agent executes |
| Critic/Verifier | Safety Agent verifies every response before delivery |
| Role-based specialisation | 6 agents with distinct responsibilities |
| Multi-step decomposition | Emotion → Risk → Context → Reason → Respond → Verify |

---

## 🖥️ Two-Mode Interface

**User Mode** — Clean, calming chat interface for people in distress. No technical metrics visible.

**Explainability Mode** — Full reasoning pipeline visible with confidence scores for judges, clinicians, researchers, and auditors.

---

## 🔍 Microsoft IQ Integration

| IQ Layer | Status | Purpose |
|---|---|---|
| Foundry IQ | ✅ Implemented | Azure AI Search knowledge base with verified mental health resources, crisis intervention protocols, coping strategies |
| Work IQ | 🔄 Roadmap | Workplace wellbeing — calendar overload, burnout detection, meeting stress patterns |
| Fabric IQ | 🔄 Roadmap | Population-level wellbeing analytics for universities, hospitals, and organisations |

---

## 🛡️ Responsible AI and Safety

MindBridge is purpose-built for a sensitive domain. Safety is not an afterthought — it is the core architecture.

- **Safety Agent** — Critic/Verifier pattern with 0-100 safety score on every response
- **Crisis detection** — Automatic HIGH risk classification with immediate crisis resource surfacing
- **UK crisis resources only** — Samaritans 116 123, Text SHOUT to 85258, Emergency 999
- **Human handoff** — Offered automatically when HIGH risk is detected
- **Microsoft.DefaultV2 Guardrail** — Jailbreak protection, content safety (hate, self-harm, sexual, violence), protected materials
- **Azure AI Content Safety** — Built into every Gen response
- **No PII** — Synthetic data only throughout

---

## 📊 Evaluation

**Synthetic evaluation dataset:** 10 test cases covering LOW, MEDIUM, and HIGH risk scenarios

| Scenario | Expected Risk | Expected Emotion |
|---|---|---|
| Anxiety and sleeplessness | LOW | Anxiety |
| Loneliness and isolation | MEDIUM | Loneliness |
| Hopelessness | MEDIUM | Depression |
| Work stress | LOW | Stress |
| Grief | LOW | Grief |
| Wondering if anyone would notice | HIGH | Crisis |
| Thoughts of self-harm | HIGH | Crisis |
| Overwhelmed and cannot cope | MEDIUM | Stress |
| Social withdrawal | MEDIUM | Depression |
| Feeling okay, just chatting | LOW | Neutral |

**AI Quality Score:** 100% (Azure AI Foundry built-in evaluation)

---

## 📡 Observability and Telemetry

- **Azure Application Insights** — Connected and active
- **Monitor dashboard** — Agent runs, token usage, cost tracking, error rate
- **Traces** — Full conversation traces via Application Insights
- **Guardrail monitoring** — Microsoft.DefaultV2 active on all model deployments
- **Scheduled evaluations** — Configured in Azure AI Foundry Monitor

---

## 🚀 Technology Stack

| Technology | Purpose |
|---|---|
| Azure AI Foundry | Agent orchestration platform |
| gpt-oss-120b (Global Standard) | Language model powering Gen |
| Azure AI Search | Foundry IQ knowledge retrieval |
| text-embedding-3-large | Knowledge base embeddings |
| Azure AI Content Safety | Built-in safety layer |
| Microsoft.DefaultV2 Guardrail | Jailbreak and content protection |
| Azure Application Insights | Telemetry and monitoring |
| Work IQ Calendar | Workplace context (connected) |
| Flask | Python web framework |
| Python 3.12 | Backend language |
| GitHub | Version control |

---

## 🏗️ Hosted Deployment Story

MindBridge is currently deployed as:
- **Gen agent** on Azure AI Foundry Agent Service (Version 8)
- **MindBridge Web App** running via Flask on Python

**Production deployment path:**
1. Package MindBridge Flask app as a Docker container
2. Push to Azure Container Registry
3. Deploy as a Hosted Agent on Foundry Agent Service
4. Assign managed identity for secure authentication
5. Expose dedicated endpoint for production traffic
6. Enable autoscaling and session state persistence

---

## 🌍 Three-Mode Vision

| Mode | Status | IQ Layer | Use Case |
|---|---|---|---|
| Individual Mode | ✅ Live | Foundry IQ | Anyone experiencing emotional distress |
| Workplace Mode | 🔄 Roadmap | Work IQ | Employees — burnout, meeting overload, workplace stress |
| Organisational Mode | 🔄 Roadmap | Fabric IQ | Universities, hospitals — population wellbeing analytics |

---

## 🔐 Security

- API keys stored in `.env` file — never committed to GitHub
- `.gitignore` excludes all secrets
- Microsoft.DefaultV2 Guardrail active on all deployments
- Synthetic data only — no PII anywhere in the system

---

## 📁 Repository Structure

```
MindBridge/
├── app.py                    # Flask backend with multi-agent orchestration
├── templates/
│   └── index.html            # Frontend with User Mode and Explainability Mode
├── .env                      # API credentials (not in GitHub)
├── .gitignore                # Excludes secrets
└── README.md                 # This file
```

---

## 👩🏾‍💻 Built By

**Onyinye Eugenia Asadu**
MSc Data Science and Artificial Intelligence — Sheffield Hallam University
Background: Database Engineer, Nigeria Interbank Settlement System (NIBSS)
Intended PhD research: Privacy-Preserving AI for Mental Health Detection

This project is a direct extension of academic purpose and professional experience — not just a hackathon entry, but the foundation of a research trajectory.

---

## 🆘 Crisis Resources

- **Samaritans (UK):** 116 123 — free, 24/7, confidential
- **Crisis Text Line:** Text SHOUT to 85258
- **Emergency:** 999
```

Paste that into README.md, save with **Ctrl + S**, then push to GitHub!