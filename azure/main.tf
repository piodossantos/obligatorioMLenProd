resource "azurerm_resource_group" "mlObli" {
  location = var.resource_group_location
  name     = var.resource_group_name
}

resource "azurerm_virtual_network" "mlObliNetwork" {
  name                = var.private_network_name
  resource_group_name = azurerm_resource_group.mlObli.name
  location            = azurerm_resource_group.mlObli.location
  address_space       = var.private_ip_range
}

resource "azurerm_storage_account" "mlObliStorage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.mlObli.name
  location                 = azurerm_resource_group.mlObli.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "mlObliStorageContainer" {
  name                  = var.storage_container_name
  storage_account_name  = azurerm_storage_account.mlObliStorage.name
  container_access_type = "private"
}

resource "azurerm_container_registry" "mlContainerRegistry" {
  name                = var.docker_registry_name
  resource_group_name = azurerm_resource_group.mlObli.name
  location            = azurerm_resource_group.mlObli.location
  sku                 = "Standard"
  admin_enabled       = true
}

resource "azurerm_log_analytics_workspace" "mlScrapperLogs" {
  name                = var.ml_scrapper_logs
  location            = azurerm_resource_group.mlObli.location
  resource_group_name = azurerm_resource_group.mlObli.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "mlScrapperEnv" {
  name                       = var.ml_scrapper_env
  location                   = azurerm_resource_group.mlObli.location
  resource_group_name        = azurerm_resource_group.mlObli.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.mlScrapperLogs.id
}
resource "azurerm_container_app" "mlScrapperApp" {
  name                         = var.ml_scrapper_app
  container_app_environment_id = azurerm_container_app_environment.mlScrapperEnv.id
  resource_group_name          = azurerm_resource_group.mlObli.name
  revision_mode                = "Single"

  template {
    container {
      name   = "scrapper"
      image  = var.scrapper_image
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
}
