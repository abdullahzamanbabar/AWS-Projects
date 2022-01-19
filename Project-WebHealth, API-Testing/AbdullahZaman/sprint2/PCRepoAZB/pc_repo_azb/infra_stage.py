from aws_cdk import core as cdk

from aws_cdk import (core,
                    aws_events,
                    aws_events_targets,
                    aws_iam, aws_sns as sns,
                    aws_cloudwatch as cw,
                    aws_sns_subscriptions as subs,
                    aws_cloudwatch_actions as cw_actions,
                    aws_dynamodb as dynamodb,
                    aws_lambda as lambda_
                    )

from pc_repo_azb.pc_repo_azb_stack import PcRepoAzbStack1

class InfraStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        infra_stack = PcRepoAzbStack1(self, 'infraStackAZB')