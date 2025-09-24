from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws.provider import AwsProvider
from imports.aws.s3_bucket import S3Bucket


class S3Stack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region="us-east-1")

        bucket = S3Bucket(
            self,
            "MyBucket",
            bucket="circleci-cdktf-bucket-123456"
        )

        TerraformOutput(self, "bucket_name", value=bucket.bucket)


app = App()
S3Stack(app, "s3-stack")
app.synth()
