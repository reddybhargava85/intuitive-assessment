# Import the needed credential and management objects from the libraries.
import os
import paramiko
from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

print(
    "Provisioning Azure Resources...some operations might take a \
minute or two."
)

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]


# Step 1: Provision a resource group

# Obtain the management object for resources, using the credentials
# from the CLI login.
resource_client = ResourceManagementClient(credential, subscription_id)

# Constants we need in multiple places: the resource group name and
# the region in which we provision resources. You can change these
# values however you want.
RESOURCE_GROUP_NAME = "Python-rg"
LOCATION = "eastus2"

# Provision the resource group.
rg_result = resource_client.resource_groups.create_or_update(
    RESOURCE_GROUP_NAME, {"location": LOCATION}
)

print(
    f"Provisioned resource group {rg_result.name} in the \
{rg_result.location} region"
)

# Step 2: provision a virtual network

# A virtual machine requires a network interface client (NIC). A NIC
# requires a virtual network and subnet along with an IP address.
# Therefore we must provision these downstream components first, then
# provision the NIC, after which we can provision the VM.

# Network and IP address names
VNET_NAME = "python-vnet"
SUBNET_NAME = "python-subnet"
IP_NAME = "python-ip"
IP_CONFIG_NAME = "python-ip-config"
NIC_NAME = "python-nic"

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

# Provision the virtual network and wait for completion
poller = network_client.virtual_networks.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {"address_prefixes": ["10.0.0.0/16"]},
    },
)

vnet_result = poller.result()

print(
    f"Provisioned virtual network {vnet_result.name} with address \
prefixes {vnet_result.address_space.address_prefixes}"
)

# Step 3: Provision the subnet and wait for completion
poller = network_client.subnets.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    SUBNET_NAME,
    {"address_prefix": "10.0.0.0/24"},
)
subnet_result = poller.result()

print(
    f"Provisioned virtual subnet {subnet_result.name} with address \
prefix {subnet_result.address_prefix}"
)


# Step 4: Provision the network interface with a private IP configuration
poller = network_client.network_interfaces.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    NIC_NAME,
    {
        "location": LOCATION,
        "ip_configurations": [
            {
                "name": IP_CONFIG_NAME,
                "subnet": {"id": subnet_result.id},
            }
        ],
    },
)

nic_result = poller.result()

print(f"Provisioned network interface client {nic_result.name}")

# Step 5: Generate an SSH Key Pair

ssh_key = paramiko.RSAKey.generate(2048)

# Step 6: Provision the virtual machine

# Obtain the management object for virtual machines
compute_client = ComputeManagementClient(credential, subscription_id)

VM_NAME = "PythonVM"
USERNAME = "azureuser"

print(
    f"Provisioning virtual machine {VM_NAME}; this operation might \
take a few minutes."
)

ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCfvjpWm2ftg3tnOEcm+6W9fIG1JYZbxRSa0vwMWg73qKjR61d548nzaMtwJiuM2Qhs/4fOM9onoY/ZInaqL1shclEma9adi3EGlP/IHY41Wow/qTR+UET58Xbva8saYddJKB8pJZsGOkjj6itZmabZasmsRwuP16fKXAnln18bh2V54gRiwBND9xakjFcQ9T0/aczWqBmXra/2HXXK+d8hBC3ja26KyfkFIEjR1UZP4ftOY2FXiH2E7uOAGaKTPfneFDUG+Rd/n5T/KqhhazswFUnN/2rHVYBiReyW6Dmzkpdk642dNLQxoGTYaVKmI4Y13JKWB9ZfRCexJozx20FAJnc7+7Zw+jKodBubW91bsTzHGk/EwFofZyPC2tyFJnZWbChkmzce/5tgEI54zxb+tQ3AfAxnTL20HW7ZOh6+IhwXsYhSZYdqKLBQEaqEAO+hj/o4ugAMettLYwWHnIf+qbSsa2mGDJVpkyxN3W9OJN/OIDkcxnJcM6yZsUVcG6k= tarakant@US-3V33XD3"


# Provision the VM specifying only minimal arguments, which defaults
# to an Ubuntu 18.04 VM on a Standard DS1 v2
# and a default virtual network/subnet.

poller = compute_client.virtual_machines.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VM_NAME,
    {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "UbuntuServer",
                "sku": "16.04.0-LTS",
                "version": "latest",
            }
        },
        "hardware_profile": {"vm_size": "Standard_DS1_v2"},
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": USERNAME,
            "linux_configuration": {
                "ssh": {
                    "publicKeys": [
                        {
                            "path": f"/home/{USERNAME}/.ssh/authorized_keys",
                            "keyData": ssh_public_key,
                        }
                    ]
                }
            },
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": nic_result.id,
                }
            ]
        },
    },
)

vm_result = poller.result()

print(f"Provisioned virtual machine {vm_result.name}")
