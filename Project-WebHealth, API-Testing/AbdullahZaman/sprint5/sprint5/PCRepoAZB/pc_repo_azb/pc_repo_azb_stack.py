from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db,
    aws_codedeploy as codedeploy,
    aws_apigateway as gateway,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr
)
from resources import constants as constants
from resources import s3bucket
from resources import sprint3_dynamo
import os

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PcRepoAzbStack1(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        ###### Storing the Json file from current environment in the bucket###########
        s3bucket.store_file("abdullahzamanbucket")
        # It reads Urls from bucket and gives a list of urls
        URL_list = s3bucket.read_file("abdullahzamanbucket", "urlsList.json")   # Used in line 87 if we want to read from bucket 
        print(URL_list)

        
        ############# WEB HEALTH and DynamoDB Lambdas ##############
        lambda_role = self.create_lambda_role()     # To allow cloudwatch and lambda access Line 146. Line 42,44
        # Web health lambda return a dictionary of avilability and latency values. Line 68
        hw_lambda = self.create_lambda("FirstHWLambda", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        # Stores the messageID and timestamp in the database
        db_lambda = self.create_lambda("DynamoLambda", "./resources", "dynamodb_lambda.lambda_handler", lambda_role)
        
        #******************** SPRINT 3 DYNAMO TABLE ****************************
        sprint3_dynamo.create_sprint3_table()   # Creating a new table to store urls from bucket
        sprint3_dynamo.putting_sprint3_data()   # Storing the urls from bucket to the table
        dynamo_sprint3_url_list = sprint3_dynamo.getting_sprint3_dynamo_data() # Line 87
        sprint3_lambda = self.create_lambda("sprint3Lambda", "./resources", "sprintt3_lambda.lambda_handler", lambda_role)
        # Making an api gateway
        api = self.create_gateway('AzbApisprint5',sprint3_lambda)
        api_resource1 = api.root.add_resource("health")     # Resource is the path with the url
        api_resource1.add_method("GET") # GET /health
        api_resource2 = api.root.add_resource("url")
        api_resource2.add_method("GET")
        api_resource2.add_method("POST")
        api_resource2.add_method("DELETE")
        api_resource2.add_method("PATCH")
        api_resource3 = api.root.add_resource("urls")
        api_resource3.add_method("GET")
        
        ############### We define the schedule, target and the rule for our lambda ################
        
        # Schedule: determines when EventBridge runs the rule
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1)) # Parameter used in Rule. Line 71
        # Target: is the recipient of Web health lambda event
        lambda_target = targets_.LambdaFunction(handler=hw_lambda)       # Parameter used in Rule. Line 71
        # Rule: specifies which targets will get our event. variable not used.
        rule = events_.Rule(self, "WebHealth_Invocation", description = "Periodic Lambda", 
                            enabled=True, schedule=lambda_schedule, targets=[lambda_target])
        
        
        
        # Creates a table for store alarms
        dynamo_table = self.create_table(os.getenv('table_name'), "AlarmDetails")   # Line: 76, 77
        dynamo_table.grant_read_write_data(db_lambda)
        db_lambda.add_environment('table_name',dynamo_table.table_name) # To give seperate names to tables
        
        # Topic: is a logical access point that acts as a communication channel
        topic = sns.Topic(self, "WebHealthTopic")   # We add alarm action on this topic. Line 117, 118, 133
        # It sends alarm to the email and dynamodb.
        topic.add_subscription(subscriptions_.EmailSubscription("abdullah.zaman.babar.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=db_lambda))
        
        
        for Url in dynamo_sprint3_url_list:
        
            dimension = {"URL" : Url}
            # This availability metric is used to generate alarm
            availability_metric = cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,
                                                metric_name=constants.URL_MONITOR_NAME_Availability+"_"+Url, 
                                                dimensions_map=dimension, 
                                                period=cdk.Duration.minutes(1), label="Availability Metric")
            # We add alarm action on latency_alarm. Line 117
            availability_alarm = cloudwatch_.Alarm(self, id="AvailabilityAlarm"+"_"+Url,
                                            metric=availability_metric,
                                            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                                            datapoints_to_alarm=1,
                                            evaluation_periods=1,
                                            threshold=1)
            
            # This latency metric is used to generate alarm                                
            latency_metric = cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,
                                                metric_name=constants.URL_MONITOR_NAME_Latency+"_"+Url, 
                                                dimensions_map=dimension, 
                                                period=cdk.Duration.minutes(1), label="Latency Metric")
            
            # We add alarm action on latency_alarm. Line 118
            latency_alarm = cloudwatch_.Alarm(self, id="LatencyAlarm"+"_"+Url,
                                            metric=latency_metric,
                                            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                            datapoints_to_alarm=1,
                                            evaluation_periods=1,
                                            threshold=0.28)
            
            availability_alarm.add_alarm_action(actions_.SnsAction(topic))
            latency_alarm.add_alarm_action(actions_.SnsAction(topic))
    
       
        ############ ROLLBACK to the previous version if an alarm is raised ##################
        metric_roll = cloudwatch_.Metric(namespace='AWS/Lambda', metric_name='Duration',    # Line 127
                                        dimensions_map={'FunctionName':hw_lambda.function_name},
                                        period= cdk.Duration.minutes(1))
    
        # Generates a rollback alarm on the rollback metric: Line 140
        alarm_roll = cloudwatch_.Alarm(self, id="RollBackAlarm", metric= metric_roll,
                                        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                        datapoints_to_alarm=1,
                                        evaluation_periods=1,
                                        threshold=2000)         # 3000 ms = 3 sec
        
        alarm_roll.add_alarm_action(actions_.SnsAction(topic))  # Line 141
       
        # Alias: is a particular version of a Web health Lambda function. 
        alias = lambda_.Alias(self, "LambdaAlias",alias_name="Lambda",version=hw_lambda.current_version) # Line 138
        
        # It deploys our 10% rollback every 1 minute
        codedeploy.LambdaDeploymentGroup(self, "WebHealth Lambda", alias=alias,
                                        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
                                        alarms=[alarm_roll]
        )
        
        ################################ Sprint 5 #################################
        vpc = ec2.Vpc.from_lookup(self, "Vpc",
                                is_default=True)
        
        cluster = ecs.Cluster(self, "AZBStackCluster2",
                            vpc=vpc)

        # Add capacity to it
        cluster.add_capacity("DefaultAutoScalingGroupCapacity",
            instance_type=ec2.InstanceType("t2.micro"),
            desired_capacity=3
        )
        ##### Defining a task for pyresttest
        task_definition = ecs.FargateTaskDefinition(self, "azbPYRESTTESTtask1", 
                        memory_limit_mib=512, cpu=256)
        
        repo = ecr.Repository.from_repository_name(self, "AZBRepo", "azb-pyresttest")
        
        task_definition.add_container("AZBpyresttestContainer",
            image=ecs.ContainerImage.from_ecr_repository(repo,tag="pyresttest"),
            memory_limit_mib=512
        )
       
        ## Instantiate an Amazon ECS Service
        ecs_service = ecs.FargateService(self, "azbPYRESTTESTservice",
            cluster=cluster,
            task_definition=task_definition
        )
        
        ######### Defining Task for Syntribos
        task_definition1 = ecs.FargateTaskDefinition(self, "azbSYNTRIBOStask1", 
                        memory_limit_mib=512, cpu=256)
        
        repo1 = ecr.Repository.from_repository_name(self, "AZBRepo1", "azb-syntribos")
        
        task_definition1.add_container("AZBsyntribosContainer",
            image=ecs.ContainerImage.from_ecr_repository(repo1,tag="syntribos"),
            memory_limit_mib=512
        )
       
        ## Instantiate an Amazon ECS Service
        ecs_service1 = ecs.FargateService(self, "azbSYNTRIBOSservice",
            cluster=cluster,
            task_definition=task_definition1
        )
        

    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
             assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('IAMFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaInvocation-DynamoDB"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayAdministrator"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSAppRunnerServicePolicyForECRAccess"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSECRPullThroughCache_ServiceRolePolicy"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceProfileForImageBuilderECRContainerBuilds"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("ECRReplicationServiceRolePolicy"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryFullAccess"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2RoleforDataPipelineRole"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2RoleforAWSCodeDeploy"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayPushToCloudWatchLogs"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("APIGatewayServiceRolePolicy"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
                
                ])
        return lambdaRole

    def create_table(self, t_name, par_key):
        try:
            return db.Table(self, id="Table", table_name=t_name,
                        partition_key=db.Attribute(name=par_key, type=db.AttributeType.STRING))
        except:
            pass
    
    def create_lambda(self, newid, asset, handler, role):
        return lambda_.Function(self, id = newid,
                                runtime = lambda_.Runtime.PYTHON_3_6,
                                handler = handler,
                                code = lambda_.Code.asset(asset),
                                role=role,
    			                    )
    
    def create_gateway(self, name, handler):
        return gateway.LambdaRestApi(self, id=name, handler=handler,
                                    proxy=False
        )
    			         
