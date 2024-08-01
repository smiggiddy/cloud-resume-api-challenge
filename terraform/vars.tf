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


variable "collection_name" {
  default = "Resumes"

}

variable "database_name" {
  default = "(default)"
}

variable "python_api_token" {
  sensitive = true
}

variable "secret_key_s3" {

}

variable "access_key_s3" {

}
