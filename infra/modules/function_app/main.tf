resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

# Storage for Function
resource "azurerm_storage_account" "func_storage" {
  name                     = "func${random_string.suffix.result}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Service Plan
resource "azurerm_service_plan" "func_plan" {
  name                = "func-plan-${random_string.suffix.result}"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

# Function App
resource "azurerm_linux_function_app" "python_func" {
  name                = "func-app-${random_string.suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name

  storage_account_name       = azurerm_storage_account.func_storage.name
  storage_account_access_key = azurerm_storage_account.func_storage.primary_access_key
  service_plan_id            = azurerm_service_plan.func_plan.id

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }

  app_settings = {
    "ENABLE_ORYX_BUILD"              = "true"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "FUNCTIONS_WORKER_RUNTIME"       = "python"
    APPLICATIONINSIGHTS_CONNECTION_STRING = var.app_insights_connection_string
  }
}
