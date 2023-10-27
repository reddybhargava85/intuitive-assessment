# Terraform Azure Infrastructure Deployment

This repository contains Terraform code that utilizes modules to deploy the following infrastructure in Azure:

- Resource Group
- Virtual Network
- Subnet
- Virtual Machines (VMs) and associated Storage Disks

## Prerequisites

Before you can deploy this infrastructure, make sure you have the following prerequisites in place:

1. **Azure Subscription**: You need an active Azure subscription. If you don't have one, you can create a [free account](https://azure.com/free) with Azure.

2. **Terraform Installed**: Ensure that Terraform is installed on your local machine. You can download it from the [official website](https://www.terraform.io/downloads.html) and follow the installation instructions.

3. **Azure CLI**: Install the Azure Command-Line Interface (CLI) and authenticate using `az login`.

## Usage

1. Clone this repository to your local machine using Git:

   ```bash
   git clone <repository_url>
   cd terraform-azure-infrastructure
   

Initialize the Terraform working directory:

bash
Copy code
terraform init
Review the Terraform plan to ensure everything is set up correctly:

bash
Copy code
terraform plan
Deploy the infrastructure to Azure:

bash
Copy code
terraform apply
Confirm the deployment by typing "yes" when prompted.

Cleanup
To destroy the deployed infrastructure when you no longer need it, run:

bash
Copy code
terraform destroy

Module Structure
This repository uses Terraform modules for better organization and reusability. You can find the modules in the respective directories.

modules/storage: Deploys the Azure Storage Account.
modules/network: Deploys the Virtual Network and its Subnets.
modules/compute: Creates Virtual Machines and attaches Storage Disks.
