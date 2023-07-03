#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_assignment.cdk_assignment_stack import CdkAssignmentStack


app = cdk.App()
CdkAssignmentStack(app, "cdk-assignment")

app.synth()
