variable "resource_group_location" {
  default     = "westus"
}

variable "private_ip_range"{
    default = ["10.0.0.0/16"]
}

variable "resource_group_name" {
  default     = "mlObli"
}

variable "private_network_name"{
    default = "mlObliNetwork"
}

variable "storage_account_name"{
    default = "mloblistorage"
}

variable "storage_container_name"{
    default = "mloblistoragecontainer"
}
variable "docker_registry_name"{
    default = "mlcontainerregistrymm278566"
}
variable "scrapper_cluster_name"{
    default = "mlscrapcluster"
}
variable "ml_scrapper_app"{
    default = "scrapperapp"
}
variable "scrapper_image"{
    default = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
}
variable "view_cluster_name"{
    default = "mlviewcluster"
}
variable "ml_view_app"{
    default = "viewapp"
}
variable "view_image"{
    default = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
}