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
  admin_enabled       = false
}