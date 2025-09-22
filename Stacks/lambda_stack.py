from constructs import Construct
from providers import AwsBaseStack
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.lambda_permission import LambdaPermission
from cdktf import AssetType, TerraformAsset
from pathlib import Path

class ComputeStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx, lambda_role_arn: str):
        super().__init__(scope, id, ctx)

        code_dir = Path("lambda_src/hello_world")
        asset = TerraformAsset(self, "lambda-zip", path=str(code_dir), type=AssetType.ARCHIVE)

        self.fn = LambdaFunction(self, "hello",
            function_name=f"{ctx.name_prefix}-hello",
            handler="app.lambda_handler",
            runtime="python3.11",
            role=lambda_role_arn,
            filename=asset.path,
            timeout=15,
            memory_size=256,
            environment={"variables": {"LOG_LEVEL": "INFO"}}
        )
