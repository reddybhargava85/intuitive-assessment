region = "eastus2"
rg-name = "rg-dev"

sa-name = "devstoraccount"
account_tier             = "Standard"
account_replication_type = "GRS"

vnet-name = "vnet"
address_space = ["10.0.0.0/16"]

address_prefixes = ["10.0.1.0/24"]

#Compute
vm-count = 2
