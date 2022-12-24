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
  name = "demo"
}

resource "aws_db_instance" "main" {
  allocated_storage       = 20
  instance_class          = "db.t4g.micro"
  engine                  = "postgres"
  engine_version          = 14.5
  username                = "postgres"
  password                = "postgres"
  backup_retention_period = 0
  db_name                 = "powerbi"
  db_subnet_group_name    = aws_db_subnet_group.main.name
  publicly_accessible     = true
  storage_type            = "gp2"
  vpc_security_group_ids  = [aws_security_group.main.id]
  skip_final_snapshot     = true
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-arm64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_ssm_parameter" "db" {
  name = "db"
  type = "String"
  value = jsonencode({
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = aws_db_instance.main.db_name
    user     = aws_db_instance.main.username
    password = aws_db_instance.main.password
  })
}

resource "aws_ssm_parameter" "ecr" {
  name = "ecr"
  type = "String"
  value = jsonencode({
    "url" : aws_ecr_repository.main.repository_url
    "registry_id" : aws_ecr_repository.main.registry_id
  })
}
resource "aws_iam_policy" "main" {
  name = "demo-policy"
  path = "/"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "VisualEditor0",
        "Effect" : "Allow",
        "Action" : "ssm:GetParameter",
        "Resource" : ["arn:aws:ssm:us-east-1:111263457661:parameter/ecr", "arn:aws:ssm:us-east-1:111263457661:parameter/db"]
      },
      {
        "Sid" : "VisualEditor1",
        "Effect" : "Allow",
        "Action" : [
          "ssm:DescribeParameters",
          "ecr:GetAuthorizationToken"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "asd",
        "Effect" : "Allow",
        "Action" : [
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ],
        "Resource" : "arn:aws:ecr:us-east-1:111263457661:repository/demo"
      }
    ]
  })
}
resource "aws_iam_role" "main" {
  name = "demo-role"
  path = "/"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
  managed_policy_arns = [aws_iam_policy.main.arn]
}
resource "aws_iam_instance_profile" "main" {
  role = aws_iam_role.main.name
}
resource "aws_instance" "main" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t4g.medium"

  credit_specification {
    cpu_credits = "unlimited"
  }

  associate_public_ip_address = true
  key_name                    = "ec2"
  vpc_security_group_ids      = [aws_security_group.main.id]
  subnet_id                   = aws_subnet.a.id
  iam_instance_profile        = aws_iam_instance_profile.main.name
}