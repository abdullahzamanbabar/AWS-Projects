from aws_cdk import(
    core,
    aws_codepipeline_actions as cpactions,
    pipelines,
    aws_iam
)
from pc_repo_azb.infra_stage import InfraStage

class PipelineStack(core.Stack):
    def __init__(self, scope:core.Construct, id:str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        pipeline_role=self.create_role()
        iam_=aws_iam.PolicyStatement(resources=['*'],actions=['iam:*'])
        sts_=aws_iam.PolicyStatement(resources=['*'],actions=['sts:*'])
        
        
        source = pipelines.CodePipelineSource.git_hub(repo_string="abdullah2021skipq/ProximaCentauri", branch='main',
                authentication=core.SecretValue.secrets_manager('Abdullah_token'),
                trigger=cpactions.GitHubTrigger.POLL
                )
                
        
        synth = pipelines.CodeBuildStep('synth', input=source,
                commands = [
                "cd AbdullahZaman/sprint3/PCRepoAZB", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
            primary_output_directory="AbdullahZaman/sprint3/PCRepoAZB/cdk.out",
            role=pipeline_role,
            role_policy_statements=[iam_,sts_]
                )
                
        
        pipeline = pipelines.CodePipeline(self, 'Pipeline', synth=synth)
        
        
        beta = InfraStage(self, "AbdullahBetaSPRINT3", env={
        'account': '315997497220',
        'region': 'us-east-2'
        })
     
        """
        production = InfraStage(self, "AbdullahProductionSPRINT3", env={
        'account': '315997497220',
        'region': 'us-east-2'
        })
        
        """
        
        unitTest = pipelines.CodeBuildStep(
            'unit_tests',input=source,
            commands=["cd AbdullahZaman/sprint3/PCRepoAZB/","pip install -r requirements.txt", "npm install -g aws-cdk", "pytest unit_tests"],
            role=pipeline_role,
            role_policy_statements=[iam_,sts_]
            )
            
        integrationTest = pipelines.CodeBuildStep(
            'integration_tests',input=source,
            commands=["cd AbdullahZaman/sprint3/PCRepoAZB/","pip install -r requirements.txt", "npm install -g aws-cdk", "pytest integration_tests"],
            role=pipeline_role,
            role_policy_statements=[iam_,sts_]
            )
        
        pipeline.add_stage(beta, pre=[unitTest] ,post=[integrationTest])
       # pipeline.add_stage(production, pre=[pipelines.ManualApprovalStep("Approve Changes and deploy to Production")])
        
        
        
        
    def create_role(self):
        role=aws_iam.Role(self,"pipeline-role",
        assumed_by=aws_iam.CompositePrincipal(
            aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            aws_iam.ServicePrincipal("sns.amazonaws.com"),
            aws_iam.ServicePrincipal("codebuild.amazonaws.com")
            ),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayAdministrator"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
            #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayPushToCloudWatchLogs"),
            #aws_iam.ManagedPolicy.from_aws_managed_policy_name("APIGatewayServiceRolePolicy"),
            #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaInvocation-DynamoDB"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ])
        return role
        