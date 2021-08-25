data "aws_ami" "amazon2" {
  owners      = ["amazon"]
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-2.0.20210721.2-x86_64-gp2"]
  }
}

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

resource "aws_instance" "elb_instance_manager_instance" {
  ami                    = data.aws_ami.amazon2.id
  instance_type          = "t3.micro"
  subnet_id              = var.public_subnet_ids[0]
  vpc_security_group_ids = [aws_security_group.elb_instance_manager_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.elb_instance_manager_instance_profile.name

  user_data = templatefile("${path.module}/templates/userdata.sh", {
    docker_image = var.docker_image
    region       = var.region
  })

  root_block_device {
    volume_type           = "gp2"
    volume_size           = "10"
    delete_on_termination = true

    tags = {
      Name = "elb-instance-manager"
    }
  }

  tags = {
    Name = "elb-instance-manager"
  }
}
