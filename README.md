# Jenkins + Terraform + Ansible

This project demonstrates a CI/CD pipeline using Jenkins to provision infrastructure on AWS with Terraform and configure it with Ansible.

## Features

- **Infrastructure as Code:** Uses Terraform to define and manage AWS resources.
- **Configuration Management:** Uses Ansible to configure the provisioned servers.
- **CI/CD Pipeline:** Automates the entire process from linting and validation to deployment.
- **Dynamic Inventory:** Generates an Ansible inventory file from the Terraform output.

## Prerequisites

Before you can run this pipeline, you'll need the following:

- **Jenkins:** A running Jenkins instance.
- **Terraform:** Terraform installed on the Jenkins agent.
- **Ansible:** Ansible installed on the Jenkins agent.
- **AWS Credentials:** An AWS account and an IAM user with programmatic access. The credentials should be stored in Jenkins as a "Username and password" credential with the ID `aws-keys`.
- **SSH Key:** An SSH key pair for accessing the EC2 instances. The private key should be stored in Jenkins as an "SSH Username with private key" credential with the ID `ansible-ssh-key`.

## Usage

1. **Fork this repository.**
2. **Create a new Pipeline job in Jenkins.**
3. **Configure the job to use "Pipeline script from SCM".**
4. **Set the SCM to "Git" and provide the URL of your forked repository.**
5. **Run the pipeline.**

The pipeline will:
1. Checkout the code.
2. Lint and validate the Terraform and Ansible code.
3. Create a Terraform plan.
4. Wait for manual approval to apply the plan.
5. Apply the Terraform plan to create the AWS resources.
6. Generate an Ansible inventory file.
7. Run an Ansible playbook to configure the EC2 instances.
8. Run a smoke test.

## Codebase Structure

```
.
├── Jenkinsfile
├── .gitignore
├── ansible
│   └── playbook.yml
├── scripts
│   └── tf_to_inventory.py
└── terraform
    ├── main.tf
    ├── outputs.tf
    ├── provider.tf
    ├── variables.tf
    └── backend.tf
    
```

- `Jenkinsfile`: The Jenkins pipeline definition.
- `ansible/playbook.yml`: The Ansible playbook to install and configure Nginx.
- `scripts/tf_to_inventory.py`: A Python script to convert Terraform output to an Ansible inventory file.
- `terraform/main.tf`: The main Terraform configuration file that defines the AWS resources.
- `terraform/outputs.tf`: Defines the output variables from Terraform.
- `terraform/provider.tf`: Configures the AWS provider for Terraform.
- `terraform/variables.tf`: Defines the input variables for Terraform.
- `terraform/backend.tf`: Defines the s3 backend to lock state in remote for Terraform.

## Manual Local Execution

You can also run the Terraform and Ansible scripts manually from your local machine.

### Prerequisites

- **Terraform:** [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- **Ansible:** [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- **AWS CLI:** [Install and configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) with your credentials.
- **SSH Key:** An SSH key pair. You'll need to add the public key to your AWS account.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abhishekpanda0620/jenkins-terraform-ansible.git
    cd jenkins-terraform-ansible
    ```

2.  **Provision infrastructure with Terraform:**
    - Navigate to the Terraform directory:
      ```bash
      cd terraform
      ```
    - Create a `terraform.tfvars` file to provide values for the variables. For example:
      ```
      key_name = "your-key-name"
      ```
    - Initialize Terraform:
      ```bash
      terraform init
      ```
    - Plan the deployment:
      ```bash
      terraform plan
      ```
    - Apply the changes:
      ```bash
      terraform apply -auto-approve
      ```
    - Get the output in JSON format:
        ```bash
        terraform output -json > ../tf_output.json
        cd ..
        ```

3.  **Generate Ansible Inventory:**
    ```bash
    python3 scripts/tf_to_inventory.py
    ```

4.  **Configure servers with Ansible:**
    Make sure you are in the root directory of the project.
    ```bash
    ansible-playbook -i inventory.ini --private-key /path/to/your/private/key ansible/playbook.yml
    ```
    Replace `/path/to/your/private/key` with the actual path to your private SSH key.

5.  **Destroy the infrastructure:**
    When you are finished, you can destroy the infrastructure to avoid incurring costs:
    ```bash
    cd terraform
    terraform destroy -auto-approve
    ```
