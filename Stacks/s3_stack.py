from constructs import Construct
from cdktf import TerraformStack
from imports.aws import AwsProvider, s3

class S3Stack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Add AWS provider
        AwsProvider(self, "AWS", region="us-east-1")

        # Create an S3 bucket
        s3.S3Bucket(self, "MyBucket",
            bucket="my-unique-bucket-name-12345",  # must be globally unique
            acl="private"
        )
