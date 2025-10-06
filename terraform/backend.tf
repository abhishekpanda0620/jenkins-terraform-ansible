terraform {
  backend "s3" {
    bucket      = "jenkins-terraform-ansible-0610"
    key         = "terraform.tfstate"
    region      = "us-east-1"
    use_lockfile = true
  }
}
