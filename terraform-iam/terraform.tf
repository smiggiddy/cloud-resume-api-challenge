terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.39.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = var.project_name
  region  = var.region
  zone    = var.zone_name
}
