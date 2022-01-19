# SPRINT3 : Build a Public CRUD API Gateway For Web-Crawler
## Overview
Creating a public CRUD API gateway endpoint to perform the create, update, delete and read the list of websites. To achieve this task: 
1. First we move the json file containing the predefined URLs from the S3 bucket to a DynamoDB database. 
2. Then we implement the CRUD REST commands on the DynamoDB entries.
3. After that we extend the tests in each stage to cover the CRUD operations.
<p align="center">
  <img src="https://github.com/abdullah2021skipq/ProximaCentauri/blob/main/AbdullahZaman/image.png" />
</p>

## AWS Services Used
1. AWS Pipelines
2. AWS Codepipeline Actions
3. AWS API Gateway
4. AWS events
5. AWS events target
6. AWS Lambda
7. AWS SNS
8. AWS Cloudwatch
9. AWS Dynamodb
10. S3 buckets

## Project Setup
To setup this project it is required to follow these steps listed below in successsion.
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
6. The API can be tested from the console using the AWS API Gateway service.
## Troubleshooting Instructions:
Pull the code to the local repository if any changes are made to the remote repository using:
```
git pull
```

## Status
Completed

## Author
Abdullah Zaman Babar  ----> DevOps Trainee at SkipQ     <abdullah.zaman.babar.s@skipq.org>
