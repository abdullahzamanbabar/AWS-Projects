# SPRINT5 : Build API test clients using pyresttest and Syntribos
## Overview
Using Docker to build API test clients using pyresttest and Syntribos. The tests will exercise the CRUD endpoints. The built images will be pushed to ECR. The API test clients will be deployed to the pipeline.

## AWS Services Used
1. AWS Pipelines
2. AWS Codepipeline Actions
3. AWS API Gateway
4. AWS Fargate
5. AWS ECS
6. AWS ECR

## Other Tools Used
1. Docker
2. pyresttest
3. Syntribos

## Project Setup
To setup this project it is required to follow these steps listed below in successsion.
1. Build a docker image:
```
docker build .
```
2. Run the image:
```
docker run <image>
```
3. Push the image:
```
docker push <image>
```
4. Any changes made locally need to be pushed to GitHub as follows:
```
git add .
```
```
git commit -m "message"
```
```
git push
```
5. The local repository can be Bootstrapped using the following command:
```
cdk bootstrap --qualifier <qualifier_name> --toolkit-stack-name <toolkit_name> aws://<account_id>/<region>
```
5. After the resources have been successfully bootstrapped, deploy the pipeline:
```
cdk deploy <pipeline_name>
```
## Troubleshooting Instructions:
In case of a timeout error during docker push, try to logout and then login again.

## Status
Complete

## Author
Abdullah Zaman Babar  ----> DevOps Trainee at SkipQ     <abdullah.zaman.babar.s@skipq.org>

