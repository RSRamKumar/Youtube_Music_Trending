provider "aws" {
  region = "eu-central-1"
}


resource "aws_s3_bucket" "landing-bucket" {
  bucket = var.landing_bucket
  force_destroy = true 
  tags = {
    name = "Youtube Project"
  }

}

resource "aws_s3_bucket" "intermediate-bucket" {
  bucket = var.intermediate_bucket
  force_destroy = true 
  tags = {
    name = "Youtube Project"
  }
}

resource "aws_s3_bucket" "transformed-bucket" {
  bucket = var.transformed_bucket
  force_destroy = true 
  tags = {
    name = "Youtube Project"
  }
}

resource "aws_s3_bucket_versioning" "transformed-bucket-versioning" {
  bucket = var.transformed_bucket
  versioning_configuration {
    status = "Enabled"
  }
}
