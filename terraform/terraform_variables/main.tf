terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = "linen-adapter-454718-k1"
  region  = "us-central1"
}



resource "google_storage_bucket" "demo-bucket" {
  name          = "linen-adapter-454718-k1-example-terraform-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

  resource "google_bigquery_dataset" "dataset" {
  dataset_id = "example_dataset_terraform"
  location   = "US"
}