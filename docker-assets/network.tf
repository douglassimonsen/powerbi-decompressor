resource "aws_vpc" "main" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_hostnames = true
}
resource "aws_internet_gateway" "main" {}
resource "aws_internet_gateway_attachment" "main" {
  internet_gateway_id = aws_internet_gateway.main.id
  vpc_id              = aws_vpc.main.id
}
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
}
resource "aws_route" "main" {
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
  route_table_id         = aws_route_table.main.id
  depends_on = [
    aws_internet_gateway_attachment.main
  ]
}
