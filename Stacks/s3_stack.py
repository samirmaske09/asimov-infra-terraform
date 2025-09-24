# Stacks/s3_stack.py
from constructs import Construct
from cdktf import TerraformStack, TerraformOutput
from imports.aws import AwsProvider, S3Bucket

class S3Stack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # AWS Provider
        AwsProvider(self, "AWS", region="us-east-1")

        # Create S3 Bucket
        bucket = S3Bucket(self, "MyDemoBucket",
            bucket="cdktf-simple-demo-bucket-123456"  # must be globally unique
        )

        # Output bucket name
        TerraformOutput(self, "bucket_name",
            value=bucket.bucket
        )
