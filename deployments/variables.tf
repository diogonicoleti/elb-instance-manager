variable "region" {
  description = "The AWS region where to create the resources"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where to create the resources"
  type        = string
}

variable "public_subnet_ids" {
  description = "The IDs of the public subnet where to create the instance and ALB"
  type        = list(string)
}
