from constructs import Construct
from providers import AwsBaseStack
from cdktf_cdktf_provider_aws.sns_topic import SnsTopic
from cdktf_cdktf_provider_aws.sqs_queue import SqsQueue

class MessagingStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx):
        super().__init__(scope, id, ctx)

        self.topic = SnsTopic(self, "events", name=f"{ctx.name_prefix}-events")
        self.queue = SqsQueue(self, "worker-queue", name=f"{ctx.name_prefix}-worker-queue")
