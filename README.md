# ⚡ OrBit — AI App Blueprint Generator

> Type what you want to build → Get a complete, validated, executable app blueprint in seconds.

---

## 🌐 Live Demo

| | URL |
|---|---|
| 🖥️ Frontend | [or-bit.vercel.app](https://or-bit.vercel.app) |
| 🔧 Backend API | [orbit-production-f7f5.up.railway.app](https://orbit-production-f7f5.up.railway.app) |
| 📖 API Docs | [/docs](https://orbit-production-f7f5.up.railway.app/docs) |

---

## 🤔 What is OrBit?

OrBit is an **AI-powered system that acts like a compiler for software generation**.

Instead of a developer spending days designing an app architecture, you simply type what you want to build in plain English — and OrBit instantly generates a complete, validated, and ready-to-use technical blueprint.

**Example:**

> "Build a project management tool with kanban board, tasks, deadlines, team roles, and notifications"

OrBit reads that sentence and produces:
- Every **page and component** the app needs
- Every **API endpoint** with request/response shapes
- Every **database table** with columns and relationships
- Every **user role** and permission rule
- All **business logic** including free vs premium limits

---

## 🧠 How It Works — 4 Stage Pipeline

OrBit processes every prompt through 4 intelligent stages, like a software compiler:

```
User Prompt
    ↓
Stage 1: Intent Extraction      → Understands what you want
    ↓
Stage 2: System Design          → Designs the app architecture
    ↓
Stage 3: Schema Generation      → Generates all 4 schemas
    ↓
Stage 4: Validation & Repair    → Finds and fixes inconsistencies
    ↓
Final Blueprint (JSON)
```

### Stage 1 — Intent Extraction
Reads the raw prompt and extracts:
- App type, features, user roles, entities
- Whether payments, analytics, or notifications are needed
- Confidence score (0–100%)
- Clarifying question if the prompt is too vague

### Stage 2 — System Design
Designs the full app architecture:
- What pages exist and how they connect
- What entities exist and how they relate
- What the user journey looks like for each role

### Stage 3 — Schema Generation
Generates 4 detailed technical blueprints:
- **UI Schema** — every page, component, form field
- **API Schema** — every endpoint, method, request/response
- **DB Schema** — every table, column, relationship
- **Auth Schema** — every role, permission, premium gate

### Stage 4 — Validation & Repair (Most Important)
Cross-checks all schemas for inconsistencies:
- Does every UI form field have a matching API endpoint?
- Does every API field exist as a DB column?
- Is every protected route covered by an auth rule?
- Are all premium features correctly gated?

When an error is found → **it repairs only that specific part**, not everything.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎯 Confidence Scoring | Shows how well the system understood your prompt |
| 📝 Assumption Logger | Documents every decision made automatically |
| 🔧 Smart Repair Engine | Fixes only broken parts, never regenerates everything |
| 🔗 Cross-Layer Checker | Ensures UI, API, DB and Auth are fully consistent |
| ⚡ 3 Generation Modes | Fast (~15s), Balanced (~30s), Quality (~60s) |
| 🚀 Runtime Simulation | Proves output is executable, not just pretty JSON |
| 📊 Evaluation Dashboard | Tracks success rate, latency, retries, failure types |

---

## 📦 What the Output Looks Like

```json
{
  "app_name": "Project Manager Pro",
  "confidence": 0.91,
  "assumptions": [
    "UUID used as primary key",
    "Free plan limited to 3 projects",
    "USD assumed as currency"
  ],
  "ui_schema": {
    "pages": ["Login", "Dashboard", "Board", "Analytics", "Settings"]
  },
  "api_schema": {
    "endpoints": ["/auth/login", "/projects", "/tasks", "/analytics"]
  },
  "db_schema": {
    "tables": ["users", "projects", "tasks", "comments", "notifications"]
  },
  "auth_schema": {
    "roles": ["super_admin", "manager", "member", "guest"],
    "permissions": { "manager": ["create_project", "assign_task"] }
  },
  "business_logic": {
    "free_limits": { "projects": 3, "members_per_project": 5 },
    "premium_features": ["analytics", "exports", "unlimited_projects"]
  },
  "validation_report": {
    "errors_found": 2,
    "errors_fixed": 2,
    "status": "clean"
  }
}
```

---

## 🛠️ Tech Stack

### Backend
| What | Tool |
|---|---|
| Language | Python |
| Framework | FastAPI |
| LLM | Groq API (llama-3.3-70b) |
| Validation | Pydantic v2 |
| Database | SQLite + SQLAlchemy |

### Frontend
| What | Tool |
|---|---|
| Framework | React.js |
| Styling | Tailwind CSS |
| Charts | Recharts |
| HTTP | Axios |

### Hosting
| What | Tool |
|---|---|
| Backend | Railway |
| Frontend | Vercel |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Backend Setup
```bash
# Clone the repo
git clone https://github.com/Nagalakshmi-N-03/OrBit.git
cd OrBit

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Start backend
python run.py
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Frontend Setup
```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

Frontend runs at: `http://localhost:3000`

---

## 📁 Project Structure

```
orbit/
├── run.py                        ← Entry point
├── requirements.txt
├── .env
│
├── backend/
│   ├── main.py                   ← FastAPI app
│   ├── config/
│   │   ├── settings.py           ← Environment config
│   │   └── database.py           ← SQLite setup
│   │
│   ├── pipeline/                 ← Core AI Logic
│   │   ├── intent_extraction.py  ← Stage 1
│   │   ├── system_design.py      ← Stage 2
│   │   ├── schema_generation.py  ← Stage 3
│   │   └── refinement.py         ← Stage 4
│   │
│   ├── validation/
│   │   ├── validator.py          ← Cross-layer checks
│   │   └── repair.py             ← Smart repair engine
│   │
│   ├── runtime/
│   │   └── simulator.py          ← Execution simulation
│   │
│   ├── evaluation/
│   │   ├── evaluator.py          ← Runs 20 test prompts
│   │   └── prompts.json          ← 10 real + 10 edge cases
│   │
│   └── routes/
│       ├── generator.py          ← Main generate endpoint
│       ├── analytics.py          ← Metrics endpoint
│       └── evaluation.py         ← Evaluation endpoint
│
└── frontend/
    └── src/
        ├── pages/
        │   ├── Generator.jsx     ← Main UI
        │   └── Analytics.jsx     ← Dashboard
        └── components/
            ├── generator/        ← Input, output, report
            └── shared/           ← Navbar, loader
```

---

## 🧪 Evaluation Framework

OrBit is tested against **20 prompts** — 10 real and 10 edge cases:

### Real Prompts (10)
- Project management tool with kanban board and team roles
- CRM with contacts, deals, and admin analytics
- E-commerce store with products, cart, and payments
- Hospital management with appointments and billing
- Food delivery app with restaurants and tracking
- ...and 5 more

### Edge Cases (10)
- **Vague:** "Build an app"
- **Conflicting:** "Make it free but charge for every feature"
- **Incomplete:** "Add a dashboard" (dashboard for what?)
- **Contradicting:** "All users are admins but restrict editing"
- **Overspecified:** 500-word prompt with every tiny detail
- ...and 5 more

### Metrics Tracked
- ✅ Success rate
- ⏱️ Average latency
- 🔁 Average retries
- ❌ Failure types

---

## ❌ What Makes This Different

| Approach | Problem |
|---|---|
| Single prompt generation | Unreliable, inconsistent output |
| No validation | Output has errors, can't be used directly |
| Full regeneration on error | Slow, expensive, loses good parts |
| **OrBit's approach** | **Multi-stage + targeted repair = reliable output** |

---

## 👩‍💻 Author

**Nagalakshmi N**


[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nagalakshmi-N-03)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nagalakshmi-n-5a7672268)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nagalakshmi.n.23003@gmail.com)
