from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    RemovalPolicy,
    aws_s3  as s3,
)
import os

class CdkAssignmentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # queue = sqs.Queue(
        #     self, "CdkAssignmentQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "CdkAssignmentTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))

        bucket_name = os.environ["MYBUCKET"]

        bucket = s3.Bucket(self, "Bucket",
            bucket_name = bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.RETAIN
        )

        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            environment={ 
                    "MYBUCKET": bucket_name
                },
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
        )

        bucket.grant_read(my_lambda)
        bucket.grant_read_write(my_lambda)
