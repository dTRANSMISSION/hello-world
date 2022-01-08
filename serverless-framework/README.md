# Serverless Framework

Serverless Framework is a command line tool that processes YAML documents to deploy code (e.g., AWS Lambda functions) and infrastructure (e.g., VPCs, Databases) that make up a serverless service.

https://github.com/serverless/serverless

## Installation/Setup

### Serverless CLI

Serverless CLI can be installed via NPM or as a standalone binary. Instructions can be found [here](https://www.serverless.com/framework/docs/getting-started)

### Serverless Plugin Install

After installing the Serverless CLI, install the plugins required for this project; to install, run the following commands in the service directly (ie. hello-world/serverless-framework/)

```bash
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-wsgi
serverless plugin install -n serverless-plugin-cloudwatch-dashboard
```

### Configure AWS Credentials

The Serverless Framework deploys to your own AWS account. You'll need to enable Serverless Framework to deploy to your AWS account by giving it access. [Here is a guide to help you set up your credentials securely](https://www.serverless.com/framework/docs/providers/aws/guide/credentials)

### Deploy the service

Enter the follwing when you have made changes to your Functions, Events or Resources in `serverless.yml` or any of the yml files in `resources/`

```bash
serverless deploy
```

### Remove the service

```bash
serverless remove
```

## Notes

### Why Serverless?

Over the last year or so, I have been leveraging AWS Lambdas to handle more and more workloads for things like slack chatbots to interact with some AWS resources, importing/exporting data to/from s3 and rds, etc; And I am often trying to find new use cases to improve my subject matter expertise in running a serverless service. From what I've experienced in implementing those solutions so far is reduced time and friction in iterating and maintenance of the services; this is likely due to the lack of complexity of my services and essentially powering them with fully AWS managed resources.

Furthermore, the code is easy to keep DRY with minimal scaffolding and configuration due to Serverless leveraging CloudFormation functions (e.g., Ref, GetAtt); no AWS account numbers, some subnet CIDRs, and only 1 ARN (for a managed IAM policy, no less) are declared in this code! This code provisions things besides the lambda function such as VPCs, subnets, routes, secrets, RDS instance, RDS proxy, API gateways and IAM roles (i.e., everything needed to make the Lambda function publically accessible was provisioned with a single `sls deploy` command once AWS credentials are delared). While, in my experience, it is possible to have a relatively DRY configuration for Terraform, in contrast, I have seen the need for much more scaffolding and configuration especially if operating in multi region.

### Experience

This is the first time I used Serverless Framework to provision more than just a Lambda function (and a Role for the Lambda) and it was very nice to only have to issue one command and tool to provision everything. However, if this Lambda Function was designed to leverage pre-existing infrastucture resources (such as VPCs, Security Groups), I would likely choose Terraform to manage the pre-existing infrastucture resources and use Serverless to manage the Lambdas to decrease the potential blast radius of a change to the Serverless code. I have not tested yet but I feel like Terraform is likely faster at updating the environment than Serverless/CloudFormation would be.

### Potential Improvements (WIP)

- Multi-region deployment leveraging GeoIP DNS
- API Gateway Caching (Not Free Tier applicable)
- `Provisioned Concurrency` for the Lambda

### Monitoring (and Observability)

By leveraging Serverless (and the `serverless-plugin-cloudwatch-dashboard`), I was able to get metrics and log groups from the Lambda function and RDS proxy for free. Due to this I opted to stick with CloudWatch.

For the Lambda I have a dashboard for the following metrics (covering p99, p95, p90, p50)

- Duration: To monitor execution time of the Lambda function.
- Errors: The error count of the function by time; this in conjunction of logs will help triage issues.
- Invocations: Implemented to count the number of function invocations.
- Throttles: This visualizes when we had an occurence of Amazon throttling our function.