resource "aws_security_group" "default_alb_sg" {
  name        = "default-alb"
  description = "Allow HTTP inbound traffic to default ALB"
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

resource "aws_lb" "default_alb" {
  name               = "default-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.default_alb_sg.id]
  subnets            = var.public_subnet_ids

  tags = {
    Name = "default-alb"
  }
}

resource "aws_lb_listener" "default_alb_http_listener" {
  load_balancer_arn = aws_lb.default_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.default_alb_http_target_group.arn
  }
}

resource "aws_lb_target_group" "default_alb_http_target_group" {
  name        = "elb-instance-manager-http"
  target_type = "instance"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  
  deregistration_delay = 5

  health_check {
    enabled  = true
    protocol = "HTTP"
    path     = "/"
    matcher  = 200
    interval = 15
  }

  tags = {
    Name = "elb-instance-manager-http"
  }
}

resource "aws_lb_target_group_attachment" "default_alb_http_target_group_attachment" {
  target_group_arn = aws_lb_target_group.default_alb_http_target_group.arn
  target_id        = aws_instance.elb_instance_manager_instance.id
  port             = 80
}
