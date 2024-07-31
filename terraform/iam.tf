locals {
  names                = ["roles/firebase.admin", "roles/cloudfunctions.admin", "roles/datastore.user"]
  excluded_permissions = concat(data.google_iam_testable_permissions.unsupported_permissions.permissions[*].name, ["resourcemanager.projects.list"])
  included_permissions = concat(flatten(values(data.google_iam_role.perms)[*].included_permissions))
  permissions          = [for permission in local.included_permissions : permission if !contains(local.excluded_permissions, permission)]
}


data "google_iam_role" "perms" {
  for_each = toset(local.names)
  name     = each.value
}

data "google_iam_policy" "admin" {
  binding {
    role = google_project_iam_custom_role.api_role.name

    members = [
      google_service_account.sa.email,
    ]
  }
}

data "google_iam_testable_permissions" "unsupported_permissions" {
  full_resource_name   = "//cloudresourcemanager.googleapis.com/projects/${var.project_name}"
  stages               = ["GA", "ALPHA", "BETA", "DEPRECATED"]
  custom_support_level = "NOT_SUPPORTED"
}

resource "google_project_iam_custom_role" "api_role" {
  role_id     = "cloudResumeApiAdmin"
  title       = "Cloud Resume API Admin"
  description = "Allows CI to CRUD actions for API"
  permissions = local.permissions
}

resource "google_service_account" "sa" {
  account_id   = var.service_account_id
  display_name = var.service_account_display_name
}


#resource "google_service_account_iam_member" "admin-account-iam" {
#  service_account_id = google_service_account.sa.name
#  role               = "projects/${var.project_name}/roles/${google_project_iam_custom_role.api_role.role_id}"
#  member             = "serviceAccount:${google_service_account.sa.email}"
#}

resource "google_service_account_iam_binding" "admin-account-iam" {
  service_account_id = google_service_account.sa.name
  role               = google_project_iam_custom_role.api_role.name

  members = [
    "serviceAccount:${google_service_account.sa.email}",
  ]

  depends_on = [google_cloudfunctions_function.function, google_cloudfunctions_function_iam_member.invoker]

  lifecycle {
    replace_triggered_by = [google_cloudfunctions_function_iam_member.invoker]
  }
}

resource "google_project_iam_binding" "service-account" {
  project = var.project_name
  role    = google_project_iam_custom_role.api_role.name
  members = [
    "serviceAccount:${google_service_account.sa.email}",
  ]

}

resource "google_service_account_key" "cloud_resume_admin_key" {
  service_account_id = google_service_account.sa.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

resource "local_sensitive_file" "sa_api_key" {
  content         = google_service_account_key.cloud_resume_admin_key.private_key
  filename        = "${path.module}/key.json"
  file_permission = "0600"
}
