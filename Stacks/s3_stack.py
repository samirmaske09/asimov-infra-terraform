from constructs import Construct
from cdktf import TerraformStack
from imports.aws import S3Bucket

class S3Stack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Example S3 bucket
        S3Bucket(self, "MyBucket",
                 bucket="my-cdktf-bucket-example-12345",
                 force_destroy=True
        )
