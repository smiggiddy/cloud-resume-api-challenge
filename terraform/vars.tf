variable "zone_name" {

}
variable "region" {

}
variable "project_name" {

}

variable "service_account_id" {

  description = "Service Account to use with GitHub Actions"
}

variable "service_account_display_name" {

}

variable "service_account_email" {

}

variable "excluded_permissions" {
  type        = list(string)
  description = "List of permissions to exclude from custom role."
  default     = []
}

