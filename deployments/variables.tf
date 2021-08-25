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

variable "docker_image" {
  description = "The ELB Instance Manager docker image to run inside the EC2 instance"
  type        = string
}

variable "docker_tag" {
  description = "The ELB Instance Manager docker image tag to run inside the EC2 instance"
  type        = string
}
