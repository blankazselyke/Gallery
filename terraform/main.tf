# Configure required providers for Google Cloud and Neon database
terraform {
  backend "gcs" {
    bucket  = "gallery-488215-terraform-state"
    prefix  = "terraform/state"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    neon = {
      source  = "kislerdm/neon"
    }
  }
}

variable "neon_api_key" {
  type        = string
  description = "A Neon API kulcs (környezeti változóból jön)"
  sensitive   = true
}

# Set up Google Cloud provider with your project ID and region
provider "google" {
  project = "gallery-488215"
  region  = "europe-west3"
}

provider "neon" {
  api_key = var.neon_api_key
}

# Create a Cloud Storage bucket to store uploaded images
resource "google_storage_bucket" "image_bucket" {
  name          = "gallery-488215-images-iac"
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true
}

# Allow public read access so images can be displayed on the website
resource "google_storage_bucket_iam_member" "public_rule" {
  bucket = google_storage_bucket.image_bucket.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# Create the Google App Engine application for the Django backend
resource "google_app_engine_application" "app" {
  project     = "gallery-488215"
  location_id = "europe-west3"
}

# Retrieve the default App Engine service account
data "google_app_engine_default_service_account" "default" {
  project    = "gallery-488215"
  depends_on = [google_app_engine_application.app]
}

# Grant the App Engine service account access to read Secret Manager secrets
resource "google_project_iam_member" "app_engine_secret_accessor" {
  project = "gallery-488215"
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${data.google_app_engine_default_service_account.default.email}"
}

# Create a new Neon project for the Django database with 1 day of history
resource "neon_project" "django_db_project" {
  name                      = "gallery-django-iac"
  history_retention_seconds = 21600
  region_id                 = "aws-eu-central-1"
  org_id                    = "org-purple-bar-69061512"
}

# Create the actual database inside the Neon project
resource "neon_database" "django_db" {
  project_id = neon_project.django_db_project.id
  branch_id  = neon_project.django_db_project.branch[0].id
  name       = "photogallery"
  owner_name = neon_project.django_db_project.branch[0].role_name
}

# Output the name of the newly created Cloud Storage bucket
output "bucket_name" {
  value = google_storage_bucket.image_bucket.name
}