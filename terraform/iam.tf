locals {
  names                = ["roles/firebase.admin", "roles/cloudfunctions.admin"]
  excluded_permissions = concat(data.google_iam_testable_permissions.unsupported_permissions.permissions[*].name)
  included_permissions = concat(flatten(values(data.google_iam_role.perms)[*].included_permissions))
  permissions          = [for permission in local.included_permissions : permission if !contains(local.excluded_permissions, permission)]
}


data "google_iam_role" "perms" {
  for_each = toset(local.names)
  name     = each.value
}

data "google_iam_policy" "admin" {
  binding {
    role = google_project_iam_custom_role.api_role.id

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
  #email        = var.service_account_email
}


resource "google_service_account_iam_policy" "admin-account-iam" {
  service_account_id = google_service_account.sa.name
  policy_data        = data.google_iam_policy.admin.policy_data
}
