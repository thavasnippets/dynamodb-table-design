variable "aws_region" {
  default = "us-east-1"
  type    = string
}

variable "environment" {
  default = "dev"
  type    = string
}

variable "account_id" {
  default = ""
  type    = string
}

variable "tags" {
  type = map(string)
}


