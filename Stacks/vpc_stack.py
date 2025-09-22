from constructs import Construct
from cdktf import TerraformStack, TerraformOutput, Fn
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.subnet import Subnet
from cdktf_cdktf_provider_aws.internet_gateway import InternetGateway
from cdktf_cdktf_provider_aws.eip import Eip
from cdktf_cdktf_provider_aws.nat_gateway import NatGateway
from cdktf_cdktf_provider_aws.route_table import RouteTable
from cdktf_cdktf_provider_aws.route import Route
from cdktf_cdktf_provider_aws.route_table_association import RouteTableAssociation
from cdktf_cdktf_provider_aws.data_aws_availability_zones import DataAwsAvailabilityZones

class NetworkStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str, config: dict):
        super().__init__(scope, ns)

        # ---------- AWS Provider ----------
        AwsProvider(self, "AWS", region=config["region"])

        # ---------- Availability Zones ----------
        azs = DataAwsAvailabilityZones(self, "azs", state="available")

        # ---------- VPC ----------
        vpc = Vpc(self, "MainVpc",
            cidr_block=config["vpc_cidr"],
            enable_dns_support=True,
            enable_dns_hostnames=True,
            tags=config["tags"],
        )

        # ---------- Subnets ----------
        public_subnet = Subnet(self, "PublicSubnet",
            vpc_id=vpc.id,
            cidr_block=config["public_subnet_cidr"],
            availability_zone=Fn.element(azs.names, 0),
            map_public_ip_on_launch=True,
            tags=config["tags"],
        )

        private_subnet = Subnet(self, "PrivateSubnet",
            vpc_id=vpc.id,
            cidr_block=config["private_subnet_cidr"],
            availability_zone=Fn.element(azs.names, 1 if len(azs.names) > 1 else 0),
            map_public_ip_on_launch=False,
            tags=config["tags"],
        )

        # ---------- Internet Gateway ----------
        igw = InternetGateway(self, "InternetGateway",
            vpc_id=vpc.id,
            tags=config["tags"],
        )

        # ---------- Elastic IP for NAT ----------
        eip = Eip(self, "NatEip",
            tags=config["tags"],
        )

        # ---------- NAT Gateway ----------
        nat_gw = NatGateway(self, "NatGateway",
            allocation_id=eip.allocation_id,
            subnet_id=public_subnet.id,
            tags=config["tags"],
        )

        # ---------- Route Tables ----------
        public_rt = RouteTable(self, "PublicRouteTable",
            vpc_id=vpc.id,
            tags=config["tags"],
        )

        private_rt = RouteTable(self, "PrivateRouteTable",
            vpc_id=vpc.id,
            tags=config["tags"],
        )

        # ---------- Routes ----------
        Route(self, "PublicDefaultRoute",
            route_table_id=public_rt.id,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=igw.id,
        )

        Route(self, "PrivateDefaultRoute",
            route_table_id=private_rt.id,
            destination_cidr_block="0.0.0.0/0",
            nat_gateway_id=nat_gw.id,
        )

        # ---------- Subnet Associations ----------
        RouteTableAssociation(self, "PublicSubnetAssociation",
            subnet_id=public_subnet.id,
            route_table_id=public_rt.id,
        )

        RouteTableAssociation(self, "PrivateSubnetAssociation",
            subnet_id=private_subnet.id,
            route_table_id=private_rt.id,
        )

        # ---------- Outputs ----------
        TerraformOutput(self, "vpc_id", value=vpc.id)
        TerraformOutput(self, "public_subnet_id", value=public_subnet.id)
        TerraformOutput(self, "private_subnet_id", value=private_subnet.id)
        TerraformOutput(self, "internet_gateway_id", value=igw.id)
        TerraformOutput(self, "nat_gateway_id", value=nat_gw.id)
        TerraformOutput(self, "nat_eip", value=eip.public_ip)