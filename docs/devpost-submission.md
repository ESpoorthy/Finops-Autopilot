# Devpost Submission — FinOps Autopilot

## 📌 Project Details

- **Project Name**: FinOps Autopilot
- **Elevator Pitch**: An autonomous AI agent that detects cloud waste, optimizes infrastructure, opens validated Terraform PRs, and proves the savings—without waiting for a human to do the busywork.
- **Repository URL**: `https://github.com/ESpoorthy/Finops-Autopilot`
- **Category**: Taskmaster (Autonomous Task Completion Agent)
- **Primary Google SDK**: Google ADK (Agent Development Kit v2.8.0)
- **Primary AI Model**: Gemini 3.5 Flash (`gemini-3.5-flash`)

---

## 🏷️ Built With Tags
`gemini-3.5-flash`, `google-adk`, `google-cloud-run`, `google-bigquery`, `google-cloud-monitoring`, `firestore`, `cloud-build`, `pubsub`, `cloud-scheduler`, `terraform`, `python`, `fastapi`

---

## 📖 About the Project

### Inspiration
Engineering organizations lose up to **30-40% of their cloud spend** on over-provisioned infrastructure (such as 12-node GKE clusters running at <25% CPU utilization). Standard FinOps platforms stop at static recommendation dashboards and alerts—leaving engineers buried in manual metric analysis, Jira ticket creation, Terraform HCL editing, and PR testing. We built **FinOps Autopilot** to bring policy-controlled autonomy to cloud cost engineering.

### What It Does
FinOps Autopilot automates the entire FinOps engineering workflow through an 8-step autonomous loop:
1. **Investigates**: Queries BigQuery billing exports (`gcp_billing_export_v1`) and Cloud Monitoring v3 utilization metrics.
2. **Reasons**: Identifies over-provisioned resources using Gemini 3.5 Flash reasoning.
3. **Optimizes**: Calculates right-sized configurations (scaling GKE nodes from 12 to 5 while maintaining >50% safety headroom).
4. **Enforces Safety Policy Guardrails**: Evaluates financial impact caps ($1,000/mo cap), confidence thresholds (80%+), and protects core categories (IAM, KMS, production DBs).
5. **Acts**: Programmatically modifies Terraform HCL code (`gke.tf`), creates a git branch, and opens a GitHub Pull Request via PyGithub.
6. **Validates**: Triggers Cloud Build staging validation (`terraform fmt`, `terraform validate`, `terraform plan`, policy checks, and pytest).
7. **Remembers**: Persists run metadata in Google Cloud Firestore (`finops_runs`) for audit trails and idempotency.
8. **Reports**: Presents financial metrics ($432/month, $5,184/year savings) on a real-time executive dashboard.

---

## ⚙️ Google Cloud Services Used
- **Google ADK (Agent Development Kit)**: Multi-agent orchestration engine (`google-adk`).
- **Gemini 3.5 Flash**: Architectural reasoning & waste analysis engine (`gemini-3.5-flash`).
- **Google Cloud Run**: Serverless container execution for backend FastAPI server.
- **Google BigQuery**: Infrastructure billing export dataset queries (`gcp_billing_export_v1`).
- **Google Cloud Monitoring v3**: Telemetry & utilization metric collector (`kubernetes.io/container/cpu/utilization`).
- **Google Cloud Firestore**: Persistent state memory & idempotency store (`finops_runs`).
- **Google Cloud Build**: Automated CI/CD staging validation pipeline (`cloudbuild.yaml`).
- **Google Cloud Pub/Sub & Cloud Scheduler**: Scheduled cron triggers and webhook handlers.

---

## 🧪 Testing Instructions

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/ESpoorthy/Finops-Autopilot.git
   cd Finops-Autopilot
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Pytest Suite**:
   ```bash
   .venv/bin/pytest tests/ -v
   ```

3. **Launch Local Executive Dashboard**:
   ```bash
   .venv/bin/python -m uvicorn backend.main:app --port 8000
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the live dashboard and run autonomous workflows.

---

## ☁️ Deployment Instructions (Google Cloud Run)

To deploy to Google Cloud Run:
```bash
gcloud config set project finops-autopilot
gcloud run deploy finops-autopilot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_MODEL=gemini-3.5-flash,DEMO_MODE=true
```
