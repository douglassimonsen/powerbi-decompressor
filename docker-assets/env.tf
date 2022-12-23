terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.48.0"
    }
  }
}
provider "aws" {
  profile = "default"
  region  = "us-east-1"
}
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
resource "aws_subnet" "a" {
  cidr_block        = "10.1.1.0/24"
  vpc_id            = aws_vpc.main.id
  availability_zone = "us-east-1a"
}
resource "aws_subnet" "b" {
  cidr_block        = "10.1.2.0/24"
  vpc_id            = aws_vpc.main.id
  availability_zone = "us-east-1b"
}
resource "aws_route_table_association" "a" {
  route_table_id = aws_route_table.main.id
  subnet_id      = aws_subnet.a.id
}
resource "aws_route_table_association" "b" {
  route_table_id = aws_route_table.main.id
  subnet_id      = aws_subnet.b.id
}
resource "aws_security_group" "main" {
  vpc_id = aws_vpc.main.id
  egress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "everything lol"
    from_port        = 0
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "-1"
    security_groups  = []
    self             = false
    to_port          = 0
  }]
  ingress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "everything lol"
    from_port        = 0
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "-1"
    security_groups  = []
    self             = false
    to_port          = 0
  }]
}
resource "aws_db_subnet_group" "main" {
  subnet_ids = [aws_subnet.a.id, aws_subnet.b.id]
}
resource "aws_ecr_repository" "main" {
  name = "test"
}

resource "aws_db_instance" "main" {
  allocated_storage       = 20
  instance_class          = "db.t4g.micro"
  engine                  = "postgres"
  engine_version          = 14.5
  username                = "postgres"
  password                = "postgres"
  backup_retention_period = 0
  identifier              = "powerbi"
  db_subnet_group_name    = aws_db_subnet_group.main.name
  publicly_accessible     = true
  storage_type            = "gp2"
  vpc_security_group_ids  = [aws_security_group.main.id]
}