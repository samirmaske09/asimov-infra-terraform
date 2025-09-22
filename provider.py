from cdktf import TerraformStack
from constructs import Construct
from cdktf_cdktf_provider_aws.provider import AwsProvider

class AwsProviderStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, region: str):
        super().__init__(scope, id)
        AwsProvider(self, "AWS", region=region)