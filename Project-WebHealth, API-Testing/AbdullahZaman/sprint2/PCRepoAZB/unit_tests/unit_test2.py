import pytest 
from aws_cdk import core
from pc_repo_azb.pc_repo_azb_stack import PcRepoAzbStack1


def test_alarm_count():
    
    app=core.App()
    PcRepoAzbStack1(app,'AlarmCount')
    template=app.synth().get_stack_by_name('AlarmCount').template
    fun=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::CloudWatch::Alarm']

    assert len(fun)==3
