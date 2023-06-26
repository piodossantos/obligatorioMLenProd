output "container_registry_admin_username" {
  value       = azurerm_container_registry.mlContainerRegistry.admin_username
  sensitive = true
}
output "container_registry_admin_password" {
  value       = azurerm_container_registry.mlContainerRegistry.admin_password
  sensitive = true
}
output "primary_blob_connection_string"{
  value = azurerm_storage_account.mlObliStorage.primary_blob_connection_string
  sensitive = true
}