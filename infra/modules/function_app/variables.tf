variable "resource_group_name" {
  type    = string
  default = "rushi-azure-infra-rg"
}
variable "location" {
  type    = string
  default = "westus2"
}
variable "app_insights_connection_string" {
  type = string
}