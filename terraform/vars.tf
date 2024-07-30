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

variable "target_level" {
  type        = string
  description = "String variable to denote if custom role being created is at project or organization level."
  default     = "project"
}

variable "excluded_permissions" {
  type        = list(string)
  description = "List of permissions to exclude from custom role."
  default     = []
}

variable "permissions" {
  type        = list(string)
  description = "IAM permissions assigned to Custom Role."
}
