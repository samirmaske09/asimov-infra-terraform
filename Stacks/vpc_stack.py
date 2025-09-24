from constructs import Construct
from cdktf import TerraformStack
from imports.aws import Vpc

class VpcStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Example VPC resource
        Vpc(self, "MyVpc",
            cidr_block="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True
        )
