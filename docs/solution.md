### Solution explained

The project contains two main parts:

- **Application**: The application code is mainly inside the `elb_instance_manager` directory and it implements from scratch the swagger spec, that is present in the `docs/swagger-file.yaml` file.
- **Infrastructure**: The infrastructure code is inside the `deployments` directory, and its a Terraform module that will create all the resources to run the ELB Instance Manager in a AWS account (ALB, Security groups, Roles, EC2, etc)

The infrastructure is basically a EC2 instance that will run the ELB Instance Manager docker image exposing it through the 80 port and exposed through an ALB called `default-alb`. It's managed by Terraform and it'll output the ALB address and instance public IP address, so you are able to use it.

The deployment is done in the following way:
- It read the `VERSION` file that contains the current application version. 
- With this value it will build and publish the docker image
- After building the image, it'll run a `terraform apply` passing the `config.json` file as variable file and a standalone variable called `docker_tag` that use the same value used to build and public the image (the one inside the `VERSION` file)

All the automation is done through the `Makefile` and the available commands as describe in the `README.md`

As I don't have much proficiency using Python to build web applications and services (I excited to learn it better!) and have a time constraint I decided to don't write unit tests.
