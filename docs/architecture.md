# FinOps Autopilot — Architecture & Technical Specifications

FinOps Autopilot is an autonomous cloud cost & architecture optimization platform built with **Google ADK (Agent Development Kit)** and **Gemini 3.5+**, deployed natively on **Google Cloud**.

---

## 🏗️ End-to-End System Architecture

```mermaid
flowchart TD
    Scheduler["⏰ Google Cloud Scheduler\n(Cron Trigger)"] -->|Pub/Sub Message| PubSub["📡 Google Cloud Pub/Sub\n(Push Topic)"]
    PubSub -->|HTTP Webhook /pubsub/trigger| CloudRun["🚀 Google Cloud Run\n(FastAPI Container Backend)"]
    
    CloudRun --> ADK["🤖 Google ADK Framework\n(google-adk)"]
    ADK --> Orchestrator["🧠 FinOps Orchestrator Agent\n(FinOpsOrchestratorAgent)"]
    Orchestrator --> Gemini["✨ Gemini 3.5+ Model\n(gemini-3.5-flash)"]

    subgraph MultiAgent ["Multi-Agent Investigation & Reasoning"]
        Orchestrator --> CostAnalyst["📊 Cost Analyst Tool"]
        CostAnalyst --> BQ["📥 BigQuery Billing Export\n(gcp_billing_export_v1)"]
        
        Orchestrator --> ArchAnalyst["📉 Architecture Analyst Tool"]
        ArchAnalyst --> Monitoring["📡 Google Cloud Monitoring v3\n(kubernetes.io/container/cpu/utilization)"]
        
        Orchestrator --> OptAgent["💡 Optimization Agent"]
    end

    subgraph Guardrails ["Safety & Policy Guardrails"]
        OptAgent --> SafetyAgent["🛡️ Safety Policy Agent"]
        SafetyAgent --> Policies["🔒 Guardrail Rules:\n- Max Monthly Change ($1,000/mo)\n- Min Confidence (80%)\n- Protected Categories (IAM, KMS, DB)"]
    end

    subgraph Action ["Autonomous Execution & Staging Validation"]
        SafetyAgent -->|PASSED| GitHubAgent["🐙 GitHub PR Agent"]
        GitHubAgent -->|Branch + HCL Patch| GitHubPR["🔀 GitHub Pull Request\n(PyGithub / Infrastructure-as-Code)"]
        
        GitHubPR -->|Webhook| CloudBuild["🏗️ Google Cloud Build"]
        CloudBuild -->|fmt / validate / plan / pytest| ValidationResult["📋 Staging Result\n(PASS / FAIL)"]
    end

    subgraph Memory ["Persistent Execution Memory & Reporting"]
        ValidationResult --> Firestore["🗄️ Google Cloud Firestore\n(finops_runs collection)"]
        Firestore --> Dashboard["📊 Executive Dashboard UI\n(FastAPI / Vanilla JS)"]
        Firestore --> Veo["🎬 Veo Executive Video Summary\n(Bonus Module)"]
    end
```

---

## 🔍 Data Flow & Step Execution

| Step | Phase | Engine / Tool | Function |
| :--- | :--- | :--- | :--- |
| **1. Trigger** | Invocation | Cloud Scheduler $\rightarrow$ Pub/Sub | Scheduled cron or manual dashboard trigger POST `/api/run-orchestrator`. |
| **2. Analyze** | Investigation | `CostAnalyst` & `ArchitectureAnalyst` | Queries BigQuery billing export and Cloud Monitoring 30-day utilization. |
| **3. Reason** | Intelligence | Gemini 3.5+ (`gemini-3.5-flash`) | Analyzes utilization metrics, identifies over-provisioning (12 $\rightarrow$ 5 nodes), synthesizes reasoning. |
| **4. Decide** | Safety Check | `SafetyAgent` | Evaluates $1,000/mo cap, 80% confidence, and protects IAM/KMS/DB resources. |
| **5. Act** | IaC Automation | `GitHubAgent` | Updates `infrastructure/terraform/gke.tf`, creates Git branch, and opens PR. |
| **6. Validate** | CI/CD Staging | `ValidationAgent` / Cloud Build | Runs `terraform fmt`, `terraform validate`, `terraform plan`, security checks, and pytest. |
| **7. Remember** | Audit Memory | `MemoryAgent` / Firestore | Saves state machine records (`finops_runs`), providing full idempotency. |
| **8. Report** | Executive UI | Dashboard | Renders financial KPIs ($432/mo, $5,184/yr savings) and live run timeline. |

---

## ⚙️ Google Cloud Infrastructure Stack

- **Reasoning Engine**: Gemini 3.5 Flash (`gemini-3.5-flash`) via `google-genai` & Google ADK `google.adk`.
- **Application Server**: Google Cloud Run (Containerized FastAPI service with auto-scaling).
- **Billing Intelligence**: Google BigQuery (`gcp_billing_export_v1`).
- **Telemetry & Metrics**: Google Cloud Monitoring v3 (`kubernetes.io/container/cpu/utilization`).
- **State & Idempotency**: Google Cloud Firestore (`finops_runs` collection).
- **Staging Pipeline**: Google Cloud Build (`cloudbuild.yaml`).
- **Event Orchestration**: Google Cloud Pub/Sub & Google Cloud Scheduler.
