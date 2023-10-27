output "vnet-name" {
  value = azurerm_virtual_network.vnet.name
}

output "nics" {
  value = [for nic in azurerm_network_interface.network-interface : nic.id]
}