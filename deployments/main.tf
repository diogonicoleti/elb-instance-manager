terraform {
  required_version = ">= 1.0.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.55.0"
    }
  }

  backend "local" {
    path = ".state/terraform.tfstate"
  }
}

provider "aws" {
  region  = var.region
  profile = "dev-staging"

  default_tags {
    tags = {
      Environment = "Test"
      Team        = "SRE"
      Project     = "ELBInstanceManager"
    }
  }
}
