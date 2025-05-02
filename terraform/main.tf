# Create CosmosDB, Azure AI Search & Blob Storage

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.27.0"
    }
  }

  required_version = ">= 1.11.4"
}

provider "azurerm" {
  features {
  }
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "azure-mcp-hackathon"
  location = "Central US"
}

# Azure AI Search Instance
resource "azurerm_search_service" "search" {
  name                = "confluentizzysearch"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "standard"
  partition_count     = 1
  replica_count       = 1
  local_authentication_enabled = true
  public_network_access_enabled = true
}

# Azure Cosmos DB (SQL API)
resource "azurerm_cosmosdb_account" "cosmosdb" {
  name                = "confluentizzycosmos"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Strong"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
}

# Cosmos DB SQL Database
resource "azurerm_cosmosdb_sql_database" "retailstore" {
  name                = "retailstore"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.cosmosdb.name

  throughput          = 400 # Provisioned throughput at the database level (optional if you want)
}

# Purchases Container
resource "azurerm_cosmosdb_sql_container" "purchases" {
  name                = "purchases"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.cosmosdb.name
  database_name       = azurerm_cosmosdb_sql_database.retailstore.name

  partition_key_paths  = ["/customer_id"]
  throughput          = 400 # optional: you can set throughput here too, or rely on database throughput
}

# Returns Container
resource "azurerm_cosmosdb_sql_container" "returns" {
  name                = "returns"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.cosmosdb.name
  database_name       = azurerm_cosmosdb_sql_database.retailstore.name

  partition_key_paths  = ["/customer_id"]
  throughput          = 400
}

# Replenishments Container
resource "azurerm_cosmosdb_sql_container" "replenishments" {
  name                = "replenishments"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.cosmosdb.name
  database_name       = azurerm_cosmosdb_sql_database.retailstore.name

  partition_key_paths  = ["/vendor_id"]
  throughput          = 400
}


# Azure Blob Storage (Storage Account)
resource "azurerm_storage_account" "storage" {
  name                     = "confluentizzyretailstore"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  account_kind             = "StorageV2"
}

# Define a list of blob container names
locals {
  container_names = [
    "departments",
    "product-pricing",
    "product-skus"
  ]
}

# Create containers using a loop
resource "azurerm_storage_container" "containers" {
  for_each              = toset(local.container_names)
  name                  = each.value
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

# Outputs (Used Later for Setting Up Confluent Resources)
output "resource_group_name" {
  description = "The name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "cosmosdb_endpoint" {
  description = "Endpoint URI for CosmosDB Account"
  value       = azurerm_cosmosdb_account.cosmosdb.endpoint
}

output "cosmosdb_account_name" {
  description = "The name of the Cosmos DB account"
  value       = azurerm_cosmosdb_account.cosmosdb.name
}

output "cosmosdb_primary_key" {
  description = "Primary key for CosmosDB Account"
  value       = azurerm_cosmosdb_account.cosmosdb.primary_key
  sensitive   = true
}

output "cosmosdb_database_name" {
  description = "The name of the Cosmos DB SQL database"
  value       = azurerm_cosmosdb_sql_database.retailstore.name
}

output "search_service_name" {
  description = "The name of the Azure AI Search instance"
  value       = azurerm_search_service.search.name
}

output "azure_search_admin_key" {
  description = "Primary Admin Key for Azure AI Search"
  value       = azurerm_search_service.search.primary_key
  sensitive   = true
}

output "azure_search_query_key" {
  description = "Primary Query Key for Azure AI Search"
  value       = azurerm_search_service.search.query_keys[0].key
  sensitive   = true
}

output "azure_search_endpoint" {
  description = "Endpoint URI for Azure AI Search"
  value       = azurerm_search_service.search.name
}

output "storage_account_name" {
  description = "The name of the storage account"
  value       = azurerm_storage_account.storage.name
}

output "storage_account_primary_access_key" {
  description = "Primary Access Key for Azure Storage Account"
  value       = azurerm_storage_account.storage.primary_access_key
  sensitive   = true
}

output "storage_account_blob_endpoint" {
  description = "Blob service endpoint for the storage account"
  value       = azurerm_storage_account.storage.primary_blob_endpoint
}

