# Devpost Submission — FinOps Autopilot

## Project Title
**FinOps Autopilot — Autonomous Cloud Cost & Architecture Optimization**

## Elevator Pitch
An autonomous AI agent built on Google ADK and Gemini 3.5+ that detects cloud waste, optimizes infrastructure, opens validated Terraform PRs, and proves financial savings—without waiting for a human engineer to do the busywork.

---

## 🚀 Inspiration
Engineering teams waste up to **30-40% of their cloud budget** on over-provisioned infrastructure (such as 12-node GKE clusters running at <25% CPU utilization). Standard FinOps tools stop at static recommendation dashboards and alerts—leaving engineers buried in manual metric analysis, Jira ticket creation, Terraform HCL editing, and PR testing. We wanted to build a true autonomous agent that executes end-to-end engineering actions safely.

---

## 💡 What It Does
FinOps Autopilot automates the entire cloud cost lifecycle through an 8-step autonomous loop:
1. **Investigates**: Queries BigQuery billing exports (`gcp_billing_export_v1`) and Cloud Monitoring v3 utilization metrics.
2. **Reasons**: Evaluates cluster telemetry using Gemini 3.5 Flash (`gemini-3.5-flash`) to detect over-provisioning (12 nodes running at 21.4% CPU utilization).
3. **Optimizes**: Calculates right-sized configurations (scaling GKE nodes from 12 to 5 while maintaining >50% safety headroom).
4. **Enforces Guardrails**: Evaluates financial impact caps ($1,000/mo cap), confidence thresholds (80%+), and protects core categories (IAM, KMS, production DBs).
5. **Acts**: Programmatically modifies Terraform HCL code (`gke.tf`), creates a git branch, and opens a GitHub Pull Request via PyGithub.
6. **Validates**: Triggers Cloud Build staging validation (`terraform fmt`, `terraform validate`, `terraform plan`, security checks, and pytest).
7. **Remembers**: Persists run metadata in Google Cloud Firestore (`finops_runs`) for audit trails and idempotency.
8. **Reports**: Presents financial metrics ($432/month, $5,184/year savings) on a real-time executive dashboard.

---

## 🛠️ How We Built It
- **Google ADK Framework**: Built multi-agent orchestration using Google ADK (`google-adk` v2.8.0).
- **Gemini 3.5+**: Leveraged `gemini-3.5-flash` for reasoning synthesis and architectural validation.
- **Google Cloud Platform**:
  - **Cloud Run**: Serverless container hosting for FastAPI backend.
  - **BigQuery & Cloud Monitoring**: Telemetry & billing export data providers.
  - **Firestore**: Persistent state store & idempotency guard (`finops_runs`).
  - **Cloud Build**: Automated CI/CD staging validation pipeline (`cloudbuild.yaml`).
  - **Cloud Scheduler & Pub/Sub**: Scheduled cron triggers and asynchronous event handling.
- **Infrastructure-as-Code & GitHub**: Autonomous HCL patching and Pull Request automation via PyGithub.

---

## 🛡️ Safety & Policy Model
FinOps Autopilot enforces **Autonomy Within Policy Boundaries**:
- Production Terraform deployment is **NEVER** performed automatically.
- All proposals require passing safety guardrails, Cloud Build staging validation, and **mandatory human engineer review and merge**.

---

## 🏆 Accomplishments That We're Proud Of
- Complete multi-agent autonomous engineering workflow from telemetry query to GitHub PR creation.
- 100% test pass rate on pytest suite.
- Clean dual-mode support (`DEMO_MODE=true` for deterministic offline hackathon demos; `DEMO_MODE=false` for live GCP environments).

---

## 🔮 What's Next for FinOps Autopilot
- Extend right-sizing agents to Cloud Storage lifecycle policies and Cloud SQL auto-pausing.
- Implement multi-region cluster scaling rules.
