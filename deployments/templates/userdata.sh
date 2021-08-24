#!/bin/bash

yum update -y
amazon-linux-extras install docker

service docker start
usermod -a -G docker ec2-user
chkconfig docker on

docker run -d -p 80:80 --restart always --name nginx nginx
