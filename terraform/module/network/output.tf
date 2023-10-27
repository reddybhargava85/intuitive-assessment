output "vnet-name" {
  value = azurerm_virtual_network.vnet.name
}

output "nics" {
  value = toset(values(azurerm_network_interface.netowrk-interface)[*].id)
}