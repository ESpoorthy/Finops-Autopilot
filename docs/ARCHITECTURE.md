# FinOps Autopilot — Architecture & Dataflow

## Overview
FinOps Autopilot is an autonomous cloud cost & architecture optimization platform powered by **Google ADK** and **Gemini 3.5+**, deployed natively on **Google Cloud**.

```mermaid
flowchart TD
    Scheduler["Cloud Scheduler"] -->|Cron Trigger| PubSub["Pub/Sub Topic"]
    PubSub -->|Push Endpoint| CloudRun["Cloud Run (FastAPI Backend)"]
    CloudRun --> ADK["Google ADK Framework"]
    ADK --> Orchestrator["FinOps Orchestrator Agent"]
    Orchestrator --> Gemini["Gemini 3.5+ Model"]

    subgraph Analysis ["Multi-Agent Investigation & Reasoning"]
        Orchestrator --> CostAnalyst["Cost Analyst Tool"]
        CostAnalyst --> BQ["BigQuery Billing Export"]
        Orchestrator --> ArchAnalyst["Architecture Analyst Tool"]
        ArchAnalyst --> Monitoring["Cloud Monitoring v3"]
        Orchestrator --> OptAgent["Optimization Agent"]
    end

    subgraph Guardrails ["Safety Policy Boundary"]
        OptAgent --> SafetyAgent["Safety Policy Agent"]
        SafetyAgent --> Policies["Configurable Safety Rules\n(Max Change, Min Confidence,\nProtected IAM/DB/KMS)"]
    end

    subgraph Action ["Autonomous Execution & Validation"]
        SafetyAgent -->|PASSED| GitHubAgent["GitHub PR Agent"]
        GitHubAgent -->|Branch + HCL Patch| GitHubPR["GitHub Pull Request"]
        GitHubPR -->|Webhook| CloudBuild["Cloud Build Staging Validation"]
        CloudBuild -->|fmt / validate / plan| ValidationResult["Staging Result: PASS / FAIL"]
    end

    subgraph Memory ["Persistent Execution Memory"]
        ValidationResult --> Firestore["Firestore (finops_runs collection)"]
        Firestore --> Dashboard["FinOps Autopilot Dashboard"]
        Firestore --> Veo["Veo Executive Video Summary (Bonus)"]
    end
```

## Core Architectural Principles

1. **Trigger to Report Autonomous Loop**:
   - Trigger -> Investigate -> Reason -> Decide -> Act -> Validate -> Record -> Report.
2. **Autonomy Within Policy Boundaries**:
   - Direct automated production terraform deployment is forbidden.
   - All infrastructure modifications are proposed as GitHub Pull Requests requiring staging validation (Cloud Build) and mandatory human merge.
3. **Dual-Mode Operational Support**:
   - `DEMO_MODE=true`: Deterministic seeded data for golden GKE right-sizing scenario ($432/mo savings, $5,184/yr, 12 -> 5 nodes).
   - `DEMO_MODE=false`: Live GCP APIs (BigQuery, Cloud Monitoring, Firestore, GitHub API).
4. **Persistent Execution Memory & Idempotency**:
   - Execution runs stored in Firestore (`finops_runs`).
   - Idempotency guard prevents duplicate PRs or repeated optimization of active resources.
