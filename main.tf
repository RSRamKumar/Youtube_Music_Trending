provider "aws" {
  region = "eu-central-1"
}


# Sample Bucket 
resource "aws_s3_bucket" "first-bucket" {
  bucket = "my-tf-test-bucket-ruppa"
  tags = {
    name = "Youtube Project"
  }
}

resource "aws_s3_bucket_versioning" "first-bucket-versioning" {
  bucket = "my-tf-test-bucket-ruppa"
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "landing-bucket" {
  bucket = "ramsur-youtube-project-01-landing-bucket"
  tags = {
    name = "Youtube Project"
  }
}

resource "aws_s3_bucket" "intermediate-bucket" {
  bucket = "ramsur-youtube-project-02-intermediate-bucket"
  tags = {
    name = "Youtube Project"
  }
}

resource "aws_s3_bucket" "transformed-bucket" {
  bucket = "ramsur-youtube-project-03-transformed-bucket"
  tags = {
    name = "Youtube Project"
  }
}
