module "function_app" {
  source = "../modules/function_app"
  app_insights_connection_string = module.monitoring.app_insights_connection_string
}

module "auth" {
  source = "../modules/auth"
}

module "monitoring" {
  source = "../modules/monitoring"
  function_app_name = module.function_app.function_app_name
}