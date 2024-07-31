# File contains manifests for Bucket and cloud function

locals {
  environment_variables = {
    GOOGLE_APPLICATION_CREDENTIALS = google_service_account_key.cloud_resume_admin_key.private_key
    COLLECTION_NAME                = var.collection_name
    DATABASE_NAME                  = var.database_name
    PROJECT_NAME                   = var.project_name

  }

}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = abspath("${path.module}/../lambda")
  output_path = abspath("${path.module}/../lambda/function.zip")
}

resource "google_storage_bucket" "bucket" {
  name     = "smigtech-bucket"
  location = "US"
}

resource "google_storage_bucket_object" "archive" {
  name       = "index.zip"
  bucket     = google_storage_bucket.bucket.name
  source     = abspath("${path.module}/../lambda/function.zip")
  depends_on = [google_storage_bucket.bucket, data.archive_file.source]
}

resource "google_cloudfunctions_function" "function" {
  name        = "cloudResumeApi"
  description = "Cloud Resume API handler Function"
  runtime     = "python39"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "http_handler"

  depends_on = [google_storage_bucket_object.archive]

  environment_variables       = local.environment_variables
  build_environment_variables = local.environment_variables

  # Attach service account to the function
  service_account_email = google_service_account.sa.email
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"

  depends_on = [google_cloudfunctions_function.function]
}

output "http_endpoint" {
  description = "Prints the Function EndPoint URL"
  value       = google_cloudfunctions_function.function.https_trigger_url
}
