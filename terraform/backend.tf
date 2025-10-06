terraform {
  backend "s3" {
    use_lockfile = true
    bucket      = "jenkins-terraform-ansible-0610"
    key         = "terraform.tfstate"
    region      = "us-east-1"
  }
}
