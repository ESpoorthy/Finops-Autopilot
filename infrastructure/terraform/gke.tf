# FinOps Autopilot Demo Infrastructure - GKE Cluster Definition
# Target file for right-sizing optimizations

resource "google_container_cluster" "primary" {
  name     = "prod-core-cluster"
  location = "us-central1"

  # We manage node pools separately
  remove_default_node_pool = true
  initial_node_count       = 5
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "default-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.primary.name
  node_count = 5

  node_config {
    preemptible  = false
    machine_type = "e2-standard-8"

    # Infrastructure tags
    labels = {
      environment = "production"
      team        = "core-infra"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
