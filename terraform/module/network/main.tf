locals {
  #loclal vars here
  local-tag = {
    cot-tag = "1.0"
  }
  subnet-name = "vm-subnet"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.name}"
  address_space       = var.address_space
  location            = var.location
  resource_group_name = var.resource_group_name

  tags = merge(local.local-tag, var.common-tags)
}

resource "azurerm_subnet" "subnet" {
  name                 = "${azurerm_virtual_network.vnet.name}-${local.subnet-name}"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.address_prefixes  
}

resource "azurerm_network_security_group" "subnet_nsg" {
  name                = "${azurerm_subnet.subnet.name}-nsg"
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_subnet_network_security_group_association" "subnet_nsg_associate" {
  depends_on = [ azurerm_network_security_rule.app_nsg_rule_inbound]  
  subnet_id                 = azurerm_subnet.subnet.id
  network_security_group_id = azurerm_network_security_group.subnet_nsg.id
}

resource "azurerm_network_interface" "netowrk-interface" {
  count = var.vm-count

  name                = "nic-${count.index}"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "vm-${count.index}"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

locals {
  app_inbound_ports_map = {
    "100" : "80", 
    "110" : "443",
    "120" : "8080",
    "130" : "22"
  } 
}

resource "azurerm_network_security_rule" "app_nsg_rule_inbound" {
  for_each = local.app_inbound_ports_map
  name                        = "Rule-Port-${each.value}"
  priority                    = each.key
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = each.value 
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.subnet_nsg.name
}
