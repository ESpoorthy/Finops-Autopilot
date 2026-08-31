# FinOps Autopilot — Autonomous Cloud Cost & Architecture Optimization

[![Google ADK](https://img.shields.io/badge/Google-ADK%202.8-4285F4?style=flat&logo=googlecloud)](https://github.com/google/adk)
[![Gemini](https://img.shields.io/badge/Gemini-3.5%2B-8E75B2?style=flat&logo=google)](https://deepmind.google/technologies/gemini/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Cloud%20Run%20%7C%20Firestore-4285F4?style=flat&logo=googlecloud)](https://cloud.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

FinOps Autopilot is an autonomous cloud cost and architecture optimization engineering agent built with **Google ADK** (Agent Development Kit) and **Gemini 3.5+**, running on **Google Cloud**.

Unlike static recommendation dashboards or simple chatbots, FinOps Autopilot executes an end-to-end autonomous engineering loop: detecting cloud resource waste from billing exports and utilization metrics, evaluating safety policies, generating production-grade Terraform HCL patches, opening GitHub Pull Requests, running Cloud Build staging validation, recording persistent state in Firestore, and reporting financial impact.

---

## 🔍 System Reality & Execution Modes

FinOps Autopilot strictly supports two operational modes:

| Feature / Tool | `DEMO_MODE=true` (Hackathon Demonstration) | `DEMO_MODE=false` (Live Production GCP) |
| :--- | :--- | :--- |
| **Cost Data** | Structured seeded billing dataset ([`demo/gke_metrics.json`](file:///Users/saispoorthyeturu/Finops-Autopilot/Finops-Autopilot-1/demo/gke_metrics.json)) | Live BigQuery Billing Export SQL query (`gcp_billing_export_v1`) |
| **Infrastructure Metrics** | Seeded 30-day GKE utilization (21.4% CPU, 28.7% Memory) | Live Google Cloud Monitoring v3 (`kubernetes.io/container/cpu/utilization`) |
| **Reasoning Engine** | Gemini 3.5+ (`google-genai` / `google.adk`) with labeled fallback | Live Gemini 3.5+ (`gemini-2.5-flash` / Vertex AI) |
| **Safety Engine** | Full Safety Agent policy evaluation (IAM/KMS/DB caps) | Full Safety Agent policy evaluation |
| **Terraform Patch** | Programmatically updates [`gke.tf`](file:///Users/saispoorthyeturu/Finops-Autopilot/Finops-Autopilot-1/infrastructure/terraform/gke.tf) (`node_count` 12 → 5) | Programmatically updates [`gke.tf`](file:///Users/saispoorthyeturu/Finops-Autopilot/Finops-Autopilot-1/infrastructure/terraform/gke.tf) |
| **GitHub Integration** | Labeled simulation mode `[SIMULATED — DEMO MODE]` (or PyGithub if `GITHUB_TOKEN` provided) | PyGithub creates Git branch, commits patch, opens Pull Request |
| **Staging Validation** | Staging execution pipeline + pytest (`[SIMULATED — DEMO MODE]`) | Google Cloud Build pipeline submission (`cloudbuild.yaml`) |
| **Execution Memory** | Persistent local JSON state ([`demo/execution_history.json`](file:///Users/saispoorthyeturu/Finops-Autopilot/Finops-Autopilot-1/demo/execution_history.json)) | Google Cloud Firestore (`finops_runs` collection) |

---

## Problem
Modern engineering teams waste up to **30-40% of their cloud budget** on over-provisioned infrastructure (such as 12-node GKE clusters running at <25% CPU/Memory utilization). Standard FinOps tools stop at static recommendation lists, leaving engineers buried in manual ticket creation, metric analysis, and Terraform updates.

## Solution
FinOps Autopilot automates the entire FinOps lifecycle through an **autonomous multi-agent architecture**:
1. **Detects Waste**: Queries BigQuery billing exports and Cloud Monitoring utilization metrics.
2. **Reasons About Optimization**: Computes safe right-sizing configurations (e.g. scaling GKE nodes from 12 to 5 while maintaining 50%+ headroom).
3. **Applies Safety Guardrails**: Evaluates financial impact caps, confidence scores, and protected resource categories (IAM, KMS, prod DBs).
4. **Acts via Infrastructure-as-Code**: Generates Terraform HCL patches, creates a git branch, and opens a GitHub Pull Request.
5. **Validates in Staging**: Triggers Cloud Build validation (`terraform fmt`, `terraform validate`, `terraform plan`, policy checks, unit tests).
6. **Remembers Execution State**: Persists run metadata in Firestore for idempotency and historical auditability.
7. **Reports Savings**: Presents financial metrics ($432/month, $5,184/year) on a polished executive dashboard.

---

## Safety Model
FinOps Autopilot enforces **Autonomy Within Policy Boundaries**:

| Guardrail Policy | Rule Description | Enforcement |
| :--- | :--- | :--- |
| **Protected Categories** | IAM, KMS, Core Networking, Encryption, Prod Databases | `SAFETY_BLOCKED` if target resource matches protected patterns |
| **Max Monthly Change** | Max financial change limit ($1,000/month cap) | `SAFETY_BLOCKED` if savings/cost exceeds threshold |
| **Min Confidence** | Minimum confidence score threshold (80%) | `SAFETY_BLOCKED` if confidence < 0.80 |
| **Staging Validation** | Cloud Build validation pipeline | Must return `PASS` |
| **Human Merge** | Production Terraform deployment | **Mandatory human engineer review & merge** |

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
GEMINI_API_KEY=your_gemini_api_key_here

# GitHub Integration
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

## Local Quickstart & Testing

1. **Activate Virtual Environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run Test Suite**:
   ```bash
   pytest tests/ -v
   ```

3. **Launch Dashboard Server**:
   ```bash
   python -m uvicorn backend.main:app --port 8000
   ```

4. **Access Dashboard**:
   Open browser at [http://localhost:8000](http://localhost:8000).

---

## License
[MIT License](LICENSE) — FinOps Autopilot Team
