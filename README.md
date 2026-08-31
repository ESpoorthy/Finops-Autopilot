# FinOps Autopilot — Autonomous Cloud Cost & Architecture Optimization

[![Google ADK](https://img.shields.io/badge/Google-ADK%202.8-4285F4?style=flat&logo=googlecloud)](https://github.com/google/adk)
[![Gemini](https://img.shields.io/badge/Gemini-3.5%2B-8E75B2?style=flat&logo=google)](https://deepmind.google/technologies/gemini/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Cloud%20Run%20%7C%20Firestore-4285F4?style=flat&logo=googlecloud)](https://cloud.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

FinOps Autopilot is an autonomous cloud cost and architecture optimization engineering agent built with **Google ADK** (Agent Development Kit) and **Gemini 3.5+**, running on **Google Cloud**.

Unlike static recommendation dashboards or simple chatbots, FinOps Autopilot executes an end-to-end autonomous engineering loop: detecting cloud resource waste from billing exports and utilization metrics, evaluating safety policies, generating production-grade Terraform HCL patches, opening GitHub Pull Requests, running Cloud Build staging validation, recording persistent state in Firestore, and reporting financial impact.

---

## Problem
Modern engineering teams waste up to **30-40% of their cloud budget** on over-provisioned infrastructure (such as 12-node GKE clusters running at <25% CPU/Memory utilization). Standard FinOps tools stop at static recommendation lists, leaving engineers buried in manual ticket creation, metric analysis, and Terraform updates.

## Solution
FinOps Autopilot automates the entire FinOps lifecycle through an **autonomous multi-agent architecture**:
1. **Detects Waste**: Queries BigQuery billing exports and Cloud Monitoring utilization metrics.
2. **Reasons About Optimization**: Computes safe right-sizing configurations (e.g. scaling GKE nodes from 12 to 5 while maintaining 60%+ headroom).
3. **Applies Safety Guardrails**: Evaluates financial impact caps, confidence scores, and protected resource categories (IAM, KMS, prod DBs).
4. **Acts via Infrastructure-as-Code**: Generates Terraform HCL patches, creates a git branch, and opens a GitHub Pull Request.
5. **Validates in Staging**: Triggers Cloud Build validation (`terraform fmt`, `terraform validate`, `terraform plan`, policy checks, unit tests).
6. **Remembers Execution State**: Persists run metadata in Firestore for idempotency and historical auditability.
7. **Reports Savings**: Presents financial metrics ($432/month, $5,184/year) on a polished executive dashboard.

## Why It Is Agentic
FinOps Autopilot is **not** a chatbot prompt wrapper or a recommendations dashboard. It is a true **autonomous agentic system**:
- **Goal-Directed Autonomy**: Triggered asynchronously via Cloud Scheduler / Pub/Sub, operating without human intervention until the PR is presented.
- **Multi-Agent Specialization**: Specialized agents for Cost Analysis, Architecture Monitoring, Safety Guardrails, Terraform Patching, GitHub PR Automation, Validation, and Persistent Memory coordinated by the **Google ADK FinOps Orchestrator**.
- **Stateful & Idempotent**: Uses Firestore execution memory to track resource states and prevent duplicate PR generation.
- **Autonomy Within Boundaries**: Operates autonomously within strict safety guardrails. Production Terraform apply strictly requires human engineer review and merge.

---

## Architecture

```
Cloud Scheduler ➔ Pub/Sub ➔ Cloud Run ➔ Google ADK ➔ FinOps Orchestrator ➔ Gemini 3.5+
                                                            │
    ┌───────────────────────────┬───────────────────────────┼───────────────────────────┐
    ▼                           ▼                           ▼                           ▼
Cost Analyst               Arch Analyst               Safety Agent               Opt Agent
    │                           │                           │                           │
BigQuery Billing         Cloud Monitoring           Policy Engine              Terraform Patch
    └───────────────────────────┴───────────────────────────┼───────────────────────────┘
                                                            ▼
                                                        GitHub PR
                                                            │
                                                       Cloud Build
                                                            │
                                                   Firestore Memory ➔ Dashboard & Veo
```

---

## Features
- 🚀 **Google ADK FinOps Orchestrator**: Modular agent architecture built on `google-adk` 2.8.0.
- 🎯 **Golden GKE Right-Sizing Scenario**: Deterministic right-sizing of over-provisioned GKE node pools (12 nodes → 5 nodes, 21.4% CPU, 28.7% Memory, $432/mo savings, $5,184/yr savings, 94% confidence).
- 🛡️ **Safety Policy Engine**: Guardrails protecting IAM, KMS, databases, and enforcing financial change caps ($1,000/mo) and confidence thresholds (80%+).
- 🐙 **GitHub PR Automation**: PyGithub wrapper creating formatted PRs with finding, evidence, configuration diffs, financial impact, safety policy result, and Cloud Build status.
- 🧪 **Cloud Build Staging Validation**: Automated validation suite (`terraform fmt`, `terraform validate`, `terraform plan`, policy assertions, unit tests).
- 💾 **Firestore Execution Memory**: Idempotent run persistence preventing duplicate optimizations.
- 📊 **Executive Dashboard**: Polished dark-mode web application (FastAPI + Vanilla CSS/JS) showing cloud spend, potential savings, validation pass rate, real-time timeline, and execution history.
- 🎥 **Veo Executive Summary Bonus**: Asynchronous video executive briefing generation (`tools/veo_agent.py`).

---

## Safety Model
FinOps Autopilot enforces **Autonomy Within Policy Boundaries**:

| Guardrail Policy | Rule Description | Enforcement |
| :--- | :--- | :--- |
| **Protected Categories** | IAM, KMS, Core Networking, Encryption, Prod Databases | `BLOCKED` if target resource matches protected patterns |
| **Max Monthly Change** | Max financial change limit ($1,000/month cap) | `BLOCKED` if savings/cost exceeds threshold |
| **Min Confidence** | Minimum confidence score threshold (80%) | `BLOCKED` if confidence < 0.80 |
| **Staging Validation** | Cloud Build validation pipeline | Must return `PASS` |
| **Human Merge** | Production Terraform deployment | **Mandatory human review & merge** |

---

## Technologies
- **AI Agent Framework**: Google ADK (`google-adk` 2.8.0)
- **AI Model**: Gemini 3.5+ (`google-genai` 2.20.0, Vertex AI / GenAI API)
- **Google Cloud Platform**: Cloud Run, Cloud Scheduler, Pub/Sub, Firestore, BigQuery, Cloud Monitoring, Cloud Build
- **Infrastructure as Code**: Terraform HCL
- **Version Control Integration**: PyGithub / GitHub REST API
- **Backend Service**: Python 3.12, FastAPI, Uvicorn, Pydantic v2
- **Testing**: pytest

---

## Project Structure
```
Finops-Autopilot/
├── agent/                  # Google ADK Orchestrator & Safety Agent
│   ├── __init__.py
│   ├── orchestrator.py    # ADK FinOps Orchestrator Agent
│   ├── safety.py          # Safety Policy Engine
│   └── prompts.py         # System prompts and templates
├── backend/                # FastAPI Application & Dashboard Server
│   ├── __init__.py
│   ├── main.py            # API routes and Pub/Sub webhook
│   ├── config.py          # Pydantic environment configuration
│   ├── models.py          # Data schemas and execution records
│   └── static/            # Dashboard web interface (HTML/CSS/JS)
│       ├── index.html
│       ├── styles.css
│       └── app.js
├── tools/                  # Agent Tools & Services
│   ├── __init__.py
│   ├── cost_analyst.py         # BigQuery billing analyst
│   ├── architecture_analyst.py # Cloud Monitoring analyst
│   ├── optimization_agent.py   # GKE right-sizing engine
│   ├── terraform_generator.py  # HCL patch modifier
│   ├── github_agent.py         # GitHub branch & PR generator
│   ├── validation_agent.py     # Cloud Build staging validator
│   ├── memory_agent.py         # Firestore execution memory
│   └── veo_agent.py            # Veo executive summary bonus
├── demo/                   # Seeded Demo Datasets
│   └── gke_metrics.json
├── infrastructure/         # Infrastructure as Code Definitions
│   ├── terraform/
│   │   └── gke.tf          # Target GKE Terraform HCL code
│   └── kubernetes/
├── tests/                  # Automated Pytest Suite
│   ├── test_safety.py
│   ├── test_optimization.py
│   ├── test_orchestrator.py
│   └── test_demo.py
├── docs/                   # Architecture & Documentation
│   └── ARCHITECTURE.md
├── cloudbuild.yaml         # Cloud Build staging validation config
├── .env.example            # Environment variables blueprint
├── requirements.txt        # Python dependency manifest
└── README.md               # Project documentation
```

---

## Environment Variables
Copy `.env.example` to `.env`:
```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=finops-autopilot-demo
GOOGLE_CLOUD_LOCATION=us-central1

# Gemini & Google ADK
GEMINI_MODEL=gemini-2.5-flash
GOOGLE_GENAI_USE_VERTEXAI=FALSE

# GitHub (Optional for DEMO_MODE)
GITHUB_TOKEN=ghp_your_github_token
GITHUB_OWNER=ESpoorthy
GITHUB_REPO=Finops-Autopilot

# Firestore
FIRESTORE_DATABASE=(default)

# Application & Safety Mode
ENVIRONMENT=development
DEMO_MODE=true
MAX_MONTHLY_CHANGE=1000.0
MIN_CONFIDENCE=0.80
```

---

## Local Setup & Quickstart

1. **Activate Virtual Environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Unit Tests**:
   ```bash
   pytest tests/
   ```

4. **Launch Dashboard & API Server**:
   ```bash
   python -m uvicorn backend.main:app --reload --port 8000
   ```

5. **Access Dashboard**:
   Open browser at [http://localhost:8000](http://localhost:8000).

---

## Demo Mode
Setting `DEMO_MODE=true` enables deterministic, reliable testing without needing live GCP billing exports or GitHub write tokens.
- **Seeded Dataset**: `demo/gke_metrics.json`
- **Simulated PR**: Formats full PR markdown body and generates simulated GitHub PR links.
- **In-Memory Store**: Tracks run states locally when Firestore credentials are not configured.

---

## Running Tests
Run the automated test suite:
```bash
pytest tests/ -v
```

Expected output:
```
tests/test_optimization.py::test_optimization_agent_golden_scenario PASSED
tests/test_optimization.py::test_terraform_generator_node_count_patch PASSED
tests/test_orchestrator.py::test_orchestrator_end_to_end_demo_run PASSED
tests/test_safety.py::test_safety_agent_allows_valid_proposal PASSED
tests/test_safety.py::test_safety_agent_blocks_protected_resource PASSED
tests/test_safety.py::test_safety_agent_blocks_low_confidence PASSED
6 passed in 1.81s
```

---

## Google Cloud Setup & Cloud Run Deployment

1. **Enable GCP APIs**:
   ```bash
   gcloud services enable run.googleapis.com \
       pubsub.googleapis.com \
       cloudscheduler.googleapis.com \
       cloudbuild.googleapis.com \
       firestore.googleapis.com \
       bigquery.googleapis.com \
       monitoring.googleapis.com
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy finops-autopilot \
       --source . \
       --region us-central1 \
       --platform managed \
       --allow-unauthenticated \
       --set-env-vars DEMO_MODE=true,GOOGLE_CLOUD_PROJECT=your-project-id
   ```

3. **Configure Pub/Sub & Cloud Scheduler**:
   ```bash
   # Create Pub/Sub topic
   gcloud pubsub topics create finops-autopilot-trigger

   # Create Cloud Scheduler job (Runs daily at 9am)
   gcloud scheduler jobs create pubsub finops-daily-job \
       --schedule="0 9 * * *" \
       --topic=finops-autopilot-trigger \
       --message-body="run"
   ```

---

## Troubleshooting
- **Missing Module `pydantic_settings`**: Run `pip install pydantic-settings`.
- **GitHub Rate Limits**: Enable `DEMO_MODE=true` in `.env` to bypass live GitHub API calls during local testing.
- **Firestore Permission Errors**: Verify `GOOGLE_APPLICATION_CREDENTIALS` points to a valid Service Account JSON key with Firestore User role.

---

## Security
- Secrets and tokens are managed exclusively via environment variables and GCP Secret Manager. `.env` is listed in `.gitignore`.
- No credentials or API keys are hardcoded in the codebase.
- Autonomous action boundaries strictly prevent automated production Terraform deployment.

---

## Limitations & Future Work
- **Current Scope**: GKE node pool right-sizing golden scenario.
- **Future Enhancements**: Cloud Storage lifecycle transition optimization, Cloud SQL idle instance auto-pause, multi-cloud AWS/Azure support, and automatic rollback on staging failure.

---

## License
[MIT License](LICENSE) — FinOps Autopilot Team
