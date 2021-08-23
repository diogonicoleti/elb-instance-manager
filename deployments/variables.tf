variable "region" {
  description = "The AWS region where to create the resources"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where to create the resources"
  type        = string
}

variable "public_subnet_id" {
  description = "The ID of the public subnet where to create the instances"
  type        = string
}
