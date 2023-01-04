resource "aws_subnet" "db_a" {
  cidr_block        = "10.1.1.0/24"
  vpc_id            = aws_vpc.main.id
  availability_zone = "us-east-1a"
}
resource "aws_subnet" "db_b" {
  cidr_block        = "10.1.2.0/24"
  vpc_id            = aws_vpc.main.id
  availability_zone = "us-east-1b"
}
resource "aws_route_table_association" "db_a" {
  route_table_id = aws_route_table.main.id
  subnet_id      = aws_subnet.db_a.id
}
resource "aws_route_table_association" "db_b" {
  route_table_id = aws_route_table.main.id
  subnet_id      = aws_subnet.db_b.id
}
resource "aws_security_group" "db" {
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
resource "aws_db_subnet_group" "db" {
  subnet_ids = [aws_subnet.db_a.id, aws_subnet.db_b.id]
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
  db_subnet_group_name    = aws_db_subnet_group.db.name
  publicly_accessible     = true
  storage_type            = "gp2"
  vpc_security_group_ids  = [aws_security_group.db.id]
  skip_final_snapshot     = true
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