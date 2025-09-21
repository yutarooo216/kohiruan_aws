# aws
provider "aws" {
  region  = "ap-northeast-1"
  profile = "default"
}

# backend
terraform {
  backend "s3" {
    bucket  = "kohiruan-reservation"
    key     = "terraform/setup.tfstate"
    region  = "ap-northeast-1"
    encrypt = true
  }
}

# data
data "aws_caller_identity" "current" {}