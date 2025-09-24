from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws.provider import AwsProvider
from imports.aws.s3_bucket import S3Bucket
from imports.aws.vpc import Vpc


class MyInfraStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # AWS provider
        AwsProvider(self, "AWS", region="us-east-1")

        # --- S3 bucket ---
        bucket = S3Bucket(
            self,
            "MyBucket",
            bucket="circleci-cdktf-bucket-12345656433"
        )

        TerraformOutput(self, "bucket_name", value=bucket.bucket)

        # --- VPC ---
        vpc = Vpc(
            self,
            "MyVpc",
            cidr_block="10.0.0.0/16"
        )

        TerraformOutput(self, "vpc_id", value=vpc.id)


app = App()
MyInfraStack(app, "infra")
app.synth()
