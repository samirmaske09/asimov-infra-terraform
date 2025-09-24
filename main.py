from cdktf import App
from Stacks.s3_stack import S3Stack

app = App()
S3Stack(app, "s3-stack")
app.synth()
