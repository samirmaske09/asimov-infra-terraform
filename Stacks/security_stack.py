from constructs import Construct
from providers import AwsBaseStack
from cdktf_cdktf_provider_aws.kms_key import KmsKey
from cdktf_cdktf_provider_aws.iam_role import IamRole
from cdktf_cdktf_provider_aws.iam_role_policy_attachment import IamRolePolicyAttachment

class SecurityStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx):
        super().__init__(scope, id, ctx)

        self.kms_key = KmsKey(self, "kms",
            description=f"{ctx.name_prefix} root KMS",
            deletion_window_in_days=7,
            enable_key_rotation=True
        )

        self.lambda_role = IamRole(self, "lambda-role",
            name=f"{ctx.name_prefix}-lambda-role",
            assume_role_policy='''{
              "Version":"2012-10-17",
              "Statement":[{
                "Effect":"Allow",
                "Principal":{"Service":"lambda.amazonaws.com"},
                "Action":"sts:AssumeRole"
              }]
            }'''
        )

        # Basic Lambda execution
        IamRolePolicyAttachment(self, "lambda-basic-exec",
            role=self.lambda_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
