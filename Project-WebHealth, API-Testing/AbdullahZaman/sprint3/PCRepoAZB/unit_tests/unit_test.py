import pytest 
from aws_cdk import core
from pc_repo_azb.pc_repo_azb_stack import PcRepoAzbStack1

def test_lambda_count():
    
    app=core.App()
    PcRepoAzbStack1(app,'Unittest')
    template=app.synth().get_stack_by_name('Unittest').template
    fun=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']

    assert len(fun)==3

    
def test_alarm_count():
    
    app=core.App()
    PcRepoAzbStack1(app,'Unittest')
    template=app.synth().get_stack_by_name('Unittest').template
    fun=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::CloudWatch::Alarm']

    assert len(fun)>=3