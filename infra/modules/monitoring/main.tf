
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

# The Database (Where logs are actually stored)
resource "azurerm_log_analytics_workspace" "main" {
  name                = "law-func-${random_string.suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# The Application Insights (The monitoring interface)
resource "azurerm_application_insights" "main" {
  name                 = "appi-func-${random_string.suffix.result}"
  location             = var.location
  resource_group_name  = var.resource_group_name
  workspace_id         = azurerm_log_analytics_workspace.main.id
  application_type     = "web"
  daily_data_cap_in_gb = 1
}

resource "azurerm_application_insights_standard_web_test" "function_health_check" {
  name                    = "ping-health-${var.function_app_name}"
  location                = var.location
  resource_group_name     = var.resource_group_name
  application_insights_id = azurerm_application_insights.main.id
  geo_locations           = ["us-fl-mia-edge"]
  frequency               = 300
  timeout                 = 30
  enabled                 = true
  retry_enabled           = true
  request {
    url = "https://${var.function_app_name}.azurewebsites.net/api/health"
  }
  validation_rules {
    expected_status_code = 200
  }
}

resource "azurerm_application_insights_workbook" "basic_dashboard" {
  name                = uuid()
  resource_group_name = var.resource_group_name
  location            = var.location
  display_name        = "Function Basic Monitor"
  source_id           = lower(azurerm_application_insights.main.id)
  data_json           = file("${path.module}/workbook.json.tpl")
  category            = "workbook"
}
