## Challenge

Your task is the following:
  - Create an API in Python that implements the spec in the [OpenAPI 2.0 file](swagger-file.yaml), you may use a code generation tool to save time, if you want to.
  - Provision a single EC2 instance and deploy your code into it using [AWS Free Tier](https://aws.amazon.com/free/).
  - The machine should be reachable via port 80 and through an ALB called `default-alb`. Ideally, we should be able to manage it via the same API you built.
  - Keep it simple.

Consider your API production ready:
  - Automate as much as possible;
  - Make your application containerized;

You are expected to provide:
  - Application code;
  - Automation code (Infrastructure, deploy, etc);
  - Documentation;
  - Separate text file (5-6 lines max) explaining your solution;

Bonus:
  - Provide integration tests.
