terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
    random = {
      source = "hashicorp/random"
      version = "~> 3.5.1"  # Specify the desired version
    }

  }
}

provider "azurerm" {
  features {}
}
