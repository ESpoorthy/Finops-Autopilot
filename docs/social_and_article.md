# Social Media & Technical Article Drafts — FinOps Autopilot

## 📱 LinkedIn / X (Twitter) Post Draft

> Built an autonomous AI cloud cost engineer with **Gemini 3.5**, **Google ADK**, and **Google Cloud**! 🚀
> 
> Most FinOps tools just give you a static recommendation list. **FinOps Autopilot** takes real engineering action safely:
> 1. Detects over-provisioned GCP infrastructure from BigQuery & Cloud Monitoring
> 2. Uses Gemini 3.5 Flash for architectural reasoning
> 3. Enforces safety policy guardrails
> 4. Updates Terraform HCL code & opens GitHub PRs
> 5. Validates changes via Cloud Build staging pipelines
> 6. Records execution state in Firestore
> 
> #AllThingsAgenticHackathon #GoogleCloud #Gemini #FinOps #AI #DevOps

---

## 📝 Technical Article Draft

### Title: Building an Autonomous FinOps Engineer with Gemini 3.5, Google ADK, and Google Cloud

*Note: This technical article was created for the purposes of entering the **All Things Agentic Hackathon**.*

#### Introduction
Cloud infrastructure waste is one of the biggest hidden costs for modern engineering organizations. Engineering teams routinely waste 30-40% of their cloud spend on over-provisioned GKE clusters, unattached persistent disks, or oversized database instances.

While conventional FinOps platforms output static dashboards, **FinOps Autopilot** introduces a new paradigm: **Policy-Controlled Autonomous Engineering**.

#### Architecture & Multi-Agent Design
Built using **Google ADK (Agent Development Kit)** and **Gemini 3.5 Flash**, FinOps Autopilot executes an 8-step autonomous loop:

1. **Telemetry Collection**: Interrogates BigQuery billing exports (`gcp_billing_export_v1`) and Cloud Monitoring v3 metrics.
2. **Gemini Reasoning**: `gemini-3.5-flash` analyzes 30-day CPU/memory utilization patterns, determining that a 12-node GKE cluster running at 21.4% CPU can be safely right-sized to 5 nodes.
3. **Safety Guardrails**: A specialized Safety Agent evaluates proposals against financial caps ($1,000/month limit), confidence thresholds (80%+), and protected resource rules (protecting IAM, KMS, and production DBs).
4. **IaC Generation & Pull Requests**: The agent programmatically updates Terraform HCL (`gke.tf`) and opens a Pull Request via PyGithub.
5. **Staging Validation**: Cloud Build executes `terraform fmt`, `terraform validate`, `terraform plan`, security checks, and pytest suites.
6. **Execution Memory**: All run records are persisted to Google Cloud Firestore (`finops_runs`), providing an immutable audit trail and preventing duplicate actions.

#### Why Autonomy Within Boundaries Matters
AI agents in production must operate within guardrails. FinOps Autopilot enforces **Autonomy Within Policy Boundaries**—meaning the agent automates research, code generation, PR creation, and staging validation, but leaves the final production apply step strictly to human engineers via GitHub PR merge.

#### Conclusion
By combining Google ADK, Gemini 3.5 Flash, Cloud Run, Firestore, and Cloud Build, FinOps Autopilot transforms passive cost monitoring into active, safe, automated cost reduction.
