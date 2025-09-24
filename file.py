#!/usr/bin/env python
from constructs import Construct
from cdktf import App

# Import your stacks
from stacks.vpc_stack import VpcStack
from stacks.s3_stack import S3Stack

app = App()

# Instantiate both stacks
VpcStack(app, "vpc")
S3Stack(app, "s3")

app.synth()
