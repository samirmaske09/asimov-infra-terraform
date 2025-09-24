from constructs import Construct
from cdktf import TerraformStack, TerraformOutput, App
from imports.aws import AwsProvider, S3Bucket


class S3Stack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Configure AWS
        AwsProvider(self, "AWS", region="us-east-1")

        # Example bucket
        bucket = S3Bucket(
            self,
            "MyBucket",
            bucket="circleci-cdktf-bucket-123456",  # must be globally unique
        )

        TerraformOutput(self, "bucket_name", value=bucket.bucket)


app = App()
S3Stack(app, "s3-stack")
app.synth()
