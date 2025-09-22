from constructs import Construct
from providers import AwsBaseStack
from cdktf_cdktf_provider_aws.api_gateway_rest_api import ApiGatewayRestApi
from cdktf_cdktf_provider_aws.api_gateway_resource import ApiGatewayResource
from cdktf_cdktf_provider_aws.api_gateway_method import ApiGatewayMethod
from cdktf_cdktf_provider_aws.api_gateway_integration import ApiGatewayIntegration
from cdktf_cdktf_provider_aws.api_gateway_deployment import ApiGatewayDeployment
from cdktf_cdktf_provider_aws.api_gateway_stage import ApiGatewayStage

class ApiStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx, lambda_arn: str):
        super().__init__(scope, id, ctx)

        self.api = ApiGatewayRestApi(self, "rest", name=f"{ctx.name_prefix}-api")
        self.resource = ApiGatewayResource(self, "hello-res",
            rest_api_id=self.api.id,
            parent_id=self.api.root_resource_id,
            path_part="hello"
        )

        self.method = ApiGatewayMethod(self, "get",
            rest_api_id=self.api.id,
            resource_id=self.resource.id,
            http_method="GET",
            authorization="NONE"
        )

        self.integration = ApiGatewayIntegration(self, "lambda-int",
            rest_api_id=self.api.id,
            resource_id=self.resource.id,
            http_method=self.method.http_method,
            integration_http_method="POST",
            type="AWS_PROXY",
            uri=f"arn:aws:apigateway:{ctx.region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
        )

        self.deployment = ApiGatewayDeployment(self, "deploy", rest_api_id=self.api.id, depends_on=[self.integration])
        self.stage = ApiGatewayStage(self, "stage", rest_api_id=self.api.id, deployment_id=self.deployment.id, stage_name=ctx.env)
