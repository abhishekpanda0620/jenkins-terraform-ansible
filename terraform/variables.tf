variable "instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 2
}
variable "ami" {
  description = "AMI ID for the EC2 instances"
  type        = string
  default     = "ami-0b0012dad04fbe3d7" # Example for Debian 13 in us-east-1
}
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
variable "key_name" {
  description = "Key pair name for SSH access"
  type        = string
  default     = "my-key-pair"
}
