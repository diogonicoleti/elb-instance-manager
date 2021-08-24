output "instance_private_ip" {
  value       = aws_instance.elb_instance_manager_instance.private_ip
  description = "The private ip generated after the instance creation"
}

output "instance_public_ip" {
  value       = aws_instance.elb_instance_manager_instance.public_ip
  description = "The public ip generated after the instance creation"
}

output "alb_url" {
  value       = "http://${aws_lb.default_alb.dns_name}"
  description = "The default application load balancer URL"
}
