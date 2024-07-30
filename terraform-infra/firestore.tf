# Using the Default Firestore to adhere to the free quota
resource "google_firestore_database" "database" {
  project     = "my-project-name"
  name        = "(default)"
  location_id = "nam5"
  type        = "FIRESTORE_NATIVE"
}

resource "google_firestore_document" "resumes" {
  project     = var.project_name
  database    = google_firestore_database.database.name
  collection  = "Resumes"
  document_id = "cloudResumeChallenge"
  fields      = jsonencode("${path.module}/firestore_schema.json")
}
