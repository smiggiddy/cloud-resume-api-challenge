terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.39.0"
    }
  }
  backend "s3" {
    endpoint                    = "us-east-1.linodeobjects.com"
    secret_key                  = var.secret_key_s3
    access_key                  = var.access_key_s3
    skip_credentials_validation = true
    bucket                      = "smiggiddy"
    key                         = "tf-gcp/state.json"
    region                      = "us-east-1"
  }

}

provider "google" {
  # Configuration options
  project = var.project_name
  region  = var.region
  zone    = var.zone_name
}
