from constructs import Construct
from providers import AwsBaseStack
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from cdktf_cdktf_provider_aws.s3_bucket_versioning import S3BucketVersioning

class StorageStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx):
        super().__init__(scope, id, ctx)

        self.data_bucket = S3Bucket(self, "data",
            bucket=f"{ctx.project}-{ctx.env}-data-bkt",
            force_destroy=False
        )

        S3BucketVersioning(self, "ver",
            bucket=self.data_bucket.id,
            versioning_configuration={"status": "Enabled"}
        )
