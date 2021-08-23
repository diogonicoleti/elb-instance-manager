resource "aws_security_group" "elb_instance_manager_sg" {
  name        = "elb-instance-manager"
  description = "Allow HTTP inbound traffic to ELB Instance Manager Service"
  vpc_id      = var.vpc_id

  ingress {
    description      = "HTTP traffic"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}
