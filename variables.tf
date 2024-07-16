
variable "landing_bucket" {
  description = "Landing Bucket Name"
  default     = "ramsur-youtube-project-01-landing-bucket"

}


variable "intermediate_bucket" {
  description = "Intermediate Bucket Name"
  default     = "ramsur-youtube-project-02-intermediate-bucket"

}

variable "transformed_bucket" {
  description = "Transformed Bucket Name"
  default     = "ramsur-youtube-project-03-transformed-bucket"

}
