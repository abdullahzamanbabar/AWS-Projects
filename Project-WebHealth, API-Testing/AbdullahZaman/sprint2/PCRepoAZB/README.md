# SPRINT2 : Continuous Integration and Continuous Deployment
## Overview
Creating a multi-stage pipeline that has a beta, gemma and production stage using 
AWS CDK. Then adding unit and integration test to the defined stages. The project 
is concluded by automating a rollback to the previous version if the metric is in 
alarm.
<p align="center">
  <img src="https://github.com/abdullah2021skipq/ProximaCentauri/blob/main/AbdullahZaman/pipeline.jpg" />
</p>

## AWS Services Used
1. AWS Pipelines
2. AWS Codepipeline Actions
3. AWS events
4. AWS events target
5. AWS Lambda
6. AWS SNS
7. AWS Cloudwatch
8. AWS Dynamodb
9. S3 buckets

## Project Setup
To setup the project it is necessary to follow the steps listed below in successsion.
1. Clone the git repository to your local environment:
```
git clone https://github.com/abdullah2021skipq/ProximaCentauri.git
```
2. Change the directory to the following:
```
cd ProximaCentauri/AbdullahZaman/sprint2/PCRepoAZB/
```
3. Any changes made locally need to be pushed to GitHub as follows:
```
git add .
```
```
git commit -m "message"
```
```
git push
```
4. The local repository can be Bootstrapped using the following command:
```
cdk bootstrap --qualifier <qualifier_name> --toolkit-stack-name <toolkit_name> aws://<account_id>/<region>
```
5. After the resources have been successfully bootstrapped, deploy the pipeline:
```
cdk deploy <pipeline_name>
```

## Troubleshooting Instructions:
Pull the code to the local repository if any changes are made to the remote repository using:
```
git pull
```

## Status
Completed

## Author
Abdullah Zaman Babar  ----> DevOps Trainee at SkipQ     <abdullah.zaman.babar.s@skipq.org>
