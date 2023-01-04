resource "aws_s3_bucket" "site" {
  bucket = var.bucket_name
}
resource "aws_s3_bucket_cors_configuration" "site" {
  bucket = aws_s3_bucket.site.id
  cors_rule {
    allowed_headers = ["Authorization", "Content-Length"]
    allowed_methods = ["GET", "POST"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}
resource "aws_s3_bucket_website_configuration" "site" {
  bucket = aws_s3_bucket.site.id
  index_document {
    suffix = "index.html"
  }
}
resource "aws_s3_bucket_acl" "site" {
  bucket = aws_s3_bucket.site.id
  acl    = "public-read"
}
resource "aws_s3_bucket_policy" "site" {
  bucket = aws_s3_bucket.site.id
  policy = templatefile("templates/s3-policy.json", { bucket = "${var.bucket_name}" })
}
resource "aws_ssm_parameter" "website" {
  name = "website"
  type = "String"
  value = jsonencode({
    bucket = var.bucket_name
  })
}