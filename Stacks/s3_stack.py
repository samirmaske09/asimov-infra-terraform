# Stacks/s3_stack.py
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws import AwsProvider, S3Bucket

class S3Stack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # AWS Provider
        AwsProvider(self, "AWS", region="us-east-1")  # change region if needed

        # Create S3 Bucket
        bucket = S3Bucket(self, "MyDemoBucket",
            bucket="cdktf-simple-demo-bucket-123456"  # must be globally unique!
        )

        # Output bucket name
        TerraformOutput(self, "bucket_name",
            value=bucket.bucket
        )

app = App()
S3Stack(app, "s3-stack")
app.synth()
