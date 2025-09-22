from constructs import Construct
from providers import AwsBaseStack
from cdktf_cdktf_provider_aws.db_subnet_group import DbSubnetGroup
from cdktf_cdktf_provider_aws.security_group import SecurityGroup
from cdktf_cdktf_provider_aws.db_instance import DbInstance

class DatabaseStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx, private_subnets: list[str], vpc_id: str, kms_key_id: str):
        super().__init__(scope, id, ctx)

        self.db_sg = SecurityGroup(self, "db-sg",
            name=f"{ctx.name_prefix}-db-sg",
            vpc_id=vpc_id,
            ingress=[{"from_port": 5432, "to_port": 5432, "protocol": "tcp", "cidr_blocks": ["10.0.0.0/8"]}],
            egress=[{"from_port": 0, "to_port": 0, "protocol": "-1", "cidr_blocks": ["0.0.0.0/0"]}]
        )

        self.subnet_group = DbSubnetGroup(self, "db-subnet",
            name=f"{ctx.name_prefix}-db-subnet",
            subnet_ids=private_subnets
        )

        self.db = DbInstance(self, "postgres",
            identifier=f"{ctx.name_prefix}-pg",
            engine="postgres",
            engine_version="15",
            allocated_storage=20,
            instance_class="db.t4g.micro",
            db_subnet_group_name=self.subnet_group.name,
            vpc_security_group_ids=[self.db_sg.id],
            storage_encrypted=True,
            kms_key_id=kms_key_id,
            username="appuser",
            password="ChangeMe_123!",
            skip_final_snapshot=True
        )
