# FinOps Autopilot — 4-Minute Demo Video Script

**Target Duration**: 3 minutes 45 seconds – 4 minutes  
**Format**: Screen recording with voiceover narration & proof of Google Cloud backend execution  

---

## ⏱️ Timeline & Presentation Flow

| Time Range | Section | Visual Focus | Voiceover & Key Talking Points |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:20** | **Problem & Value Prop** | Title Slide / Dashboard Header | *"Cloud infrastructure waste costs enterprises over $30B annually. Standard FinOps dashboards produce static recommendation lists, leaving engineers to manually analyze metrics, edit HCL code, and test PRs. Meet **FinOps Autopilot**—an autonomous AI agent built on Google ADK and Gemini 3.5+ that detects waste, updates Terraform HCL, validates changes, and records financial impact automatically."* |
| **0:20 – 0:40** | **Dashboard & DEMO_MODE** | Dashboard UI (`http://localhost:8000`) | *"Here is the Executive Dashboard. Notice the explicit `DEMO MODE` badge, guaranteeing an honest, reproducible demonstration of our golden path workflow."* |
| **0:40 – 1:10** | **Run Autonomous Workflow** | Click "Trigger Autonomous Run" | *"We trigger an autonomous optimization run for cluster `prod-core-cluster`. The agent initiates an 8-step autonomous loop."* |
| **1:10 – 1:40** | **Cost & Monitoring Analysis** | Detection Finding & Metrics Card | *"First, the agent queries BigQuery billing exports and Cloud Monitoring 30-day telemetry. It detects that `prod-core-cluster` is running 12 `e2-standard-8` nodes at only 21.4% CPU utilization and 28.7% Memory utilization."* |
| **1:40 – 2:10** | **Gemini 3.5+ Reasoning & Safety** | Finding Card & Policy Badge | *"Gemini 3.5 Flash synthesizes the architectural reasoning: scaling from 12 down to 5 nodes maintains a 50%+ safety headroom for traffic spikes while unlocking $432/month ($5,184/year) in savings. The proposal passes our Safety Agent policy guardrail with a 94% confidence score."* |
| **2:10 – 2:40** | **Terraform HCL Patch & GitHub PR** | GitHub PR Link & Code Diff | *"The agent programmatically updates `infrastructure/terraform/gke.tf`, reducing `node_count` from 12 to 5. It creates a Git branch and opens GitHub PR #17 (clearly labeled `[SIMULATED — DEMO MODE]` when running without live credentials)."* |
| **2:40 – 3:10** | **Staging Validation (Cloud Build)** | Cloud Build Badge & Staging Log | *"Next, the agent triggers Cloud Build staging validation running `terraform fmt`, `terraform validate`, `terraform plan`, security checks, and unit tests."* |
| **3:10 – 3:30** | **Financial Savings & KPI Impact** | Top KPI Cards ($432/mo, 100% Pass) | *"Upon passing staging validation, the executive dashboard updates dynamically from persistent memory—showing $432/month projected savings and 100% validation pass rate."* |
| **3:30 – 3:45** | **Execution Memory & Idempotency** | Run History Table | *"All run metadata is stored in persistent Firestore memory (`finops_runs`), enforcing idempotency so active clusters are never double-optimized."* |
| **3:45 – 4:00** | **Google Cloud Backend Proof** | GCP Cloud Run Service Console / CLI | *"FinOps Autopilot runs on Google Cloud Run with Pub/Sub push triggers. Thank you—FinOps Autopilot brings policy-controlled autonomy to cloud optimization!"* |
