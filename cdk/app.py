#!/usr/bin/env python3
from aws_cdk import App
from stacks.chat_app_stack import ChatAppStack

app = App()
ChatAppStack(app, "ChatAppStack")
app.synth()
