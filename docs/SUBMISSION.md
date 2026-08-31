# Devpost Submission — FinOps Autopilot

## Project Title
**FinOps Autopilot — Autonomous Cloud Cost & Architecture Optimization**

## Elevate Pitch
FinOps Autopilot is an autonomous cloud cost engineering agent built on Google ADK and Gemini 3.5+. It continuously monitors GCP infrastructure metrics, detects waste, enforces safety guardrails, updates Terraform HCL code, opens GitHub Pull Requests, validates changes via Cloud Build, and records persistent execution memory in Firestore.

---

## Inspiration
Engineering teams waste over $30B annually on over-provisioned cloud infrastructure. Traditional FinOps tools only output static dashboards and alerts—leaving engineers to manually investigate metrics, write Jira tickets, modify Terraform code, and test pull requests. We wanted to build a true autonomous agent that takes real engineering action safely.

---

## What It Does
FinOps Autopilot executes an 8-step autonomous engineering loop:
1. **Investigates**: Queries BigQuery billing exports and Cloud Monitoring utilization metrics.
2. **Reasons**: Identifies over-provisioned resources (e.g. GKE cluster with 12 nodes running at 21.4% CPU utilization).
3. **Optimizes**: Calculates safe right-sized configurations (scaling from 12 to 5 nodes while maintaining 60%+ headroom, saving $432/month and $5,184/year).
4. **Enforces Guardrails**: Passes proposals through a Safety Agent policy engine (blocking IAM, KMS, databases, and changes > $1,000/mo).
5. **Acts**: Generates Terraform HCL patches, creates a git branch, and opens a GitHub Pull Request.
6. **Validates**: Triggers Cloud Build staging validation (`terraform fmt`, `terraform validate`, `terraform plan`, policy checks, unit tests).
7. **Remembers**: Persists run metadata in Firestore (`finops_runs`) for idempotency and audit trails.
8. **Reports**: Displays real-time financial impact and validation status on an executive dashboard.

---

## How We Built It
- **Google ADK Framework**: Coordinated multi-agent reasoning and orchestration (`google-adk`).
- **Gemini 3.5+**: Reasoning engine for waste analysis and recommendation synthesis.
- **Google Cloud Services**:
  - **Cloud Run**: Serverless container execution for FastAPI backend.
  - **Cloud Scheduler & Pub/Sub**: Asynchronous cron triggers.
  - **Firestore**: Persistent execution memory & idempotency store.
  - **BigQuery & Cloud Monitoring**: Billing exports & infrastructure metrics.
  - **Cloud Build**: Automated staging validation pipeline.
- **Terraform & GitHub API**: Autonomous Infrastructure-as-Code modification via PyGithub.
- **FastAPI & Web Dashboard**: Executive UI displaying live execution timeline and projected savings.

---

## Challenges We Overcame
1. **Ensuring Safe Autonomy**: Giving AI systems infrastructure access can be risky. We designed an **Autonomy Within Boundaries** policy framework where all production changes stop at GitHub Pull Requests and mandatory human engineer review.
2. **Demo Reliability vs. Cloud Billing Latency**: GCP billing exports update with 24-hour latency. We implemented a dual-mode system (`DEMO_MODE=true` vs `DEMO_MODE=false`) so the end-to-end golden path runs deterministically out of the box.

---

## Accomplishments That We're Proud Of
- Implemented a complete autonomous engineering workflow—moving beyond simple recommendation chatbots.
- 100% test coverage for safety policies, GKE right-sizing calculations, and ADK orchestrator runs.
- Polished executive dashboard visually demonstrating real-time agent execution step by step.

---

## What We Learned
- How to build modular, stateful agents using Google ADK.
- How to combine deterministic policy guardrails with LLM reasoning to ensure zero production hallucination.

---

## What's Next for FinOps Autopilot
- Expand right-sizing algorithms to Cloud Storage lifecycle policies and Cloud SQL auto-pausing.
- Add multi-cloud support for AWS and Azure.
- Automatic rollback triggers on staging validation failure.
