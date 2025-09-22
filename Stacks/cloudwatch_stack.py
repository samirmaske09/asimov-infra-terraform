from constructs import Construct
from providers import AwsBaseStack
from cdktf_cdktf_provider_aws.cloudwatch_log_group import CloudwatchLogGroup
from cdktf_cdktf_provider_aws.cloudwatch_metric_alarm import CloudwatchMetricAlarm

class ObservabilityStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx, lambda_name: str):
        super().__init__(scope, id, ctx)

        self.logs = CloudwatchLogGroup(self, "lambda-lg", name=f"/aws/lambda/{lambda_name}", retention_in_days=14)

        self.alarm = CloudwatchMetricAlarm(self, "errors",
            alarm_name=f"{ctx.name_prefix}-lambda-errors",
            namespace="AWS/Lambda",
            metric_name="Errors",
            statistic="Sum",
            period=60,
            evaluation_periods=1,
            threshold=1,
            comparison_operator="GreaterThanOrEqualToThreshold",
            dimensions={"FunctionName": lambda_name}
        )
