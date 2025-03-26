import aws_cdk as core
import aws_cdk.assertions as assertions

from savvyai.savvyai_stack import savvyai

# example tests. To run these tests, uncomment this file along with the example
# resource in private_assistant_v2/private_assistant_v2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = savvyai(app, "savvyai")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
