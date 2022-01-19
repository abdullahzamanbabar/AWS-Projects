import aws_cdk as core
import aws_cdk.assertions as assertions


from pc_repo_azb.pc_repo_azb_stack import PcRepoAzbStack1


# example tests. To run these tests, uncomment this file along with the example
# resource in pc_repo_azb/pc_repo_azb_stack.py
def test_sqs_queue_created():
     app = core.App()
     stack = PcRepoAzbStack1(app, "pc-repo-azb")
     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
 #        "VisibilityTimeout": 300
  #   })
#  pass
