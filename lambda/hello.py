import json
import logging
import boto3
import os
from botocore.exceptions import ClientError

def handler(event, context):

    #dumping request for debugging purposes
    print('request: {}'.format(json.dumps(event)))
    object_flag = False
    s3_client = boto3.client('s3')
    bucket_name = os.environ['MYBUCKET']
    # specify bucket name using envoirnment variable
    # bucket_name = 'cdk-workshop-bucket83908e77-ag5nqfjjz7lf'
    # object_name = 'order_with_status.csv'

    # getting object name using string parameters
    object_name = event['queryStringParameters']['object_name']

    # getting presigned url 
    response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=3600)
    
    # check if object exists
    try:
        s3 = boto3.resource('s3')
        s3.Object(bucket_name, object_name).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            ...
        else:
            # Something else has gone wrong.
            raise
    else:
        # The object does exist.
        object_flag = True

    # testing object if exists in s3
    # response = s3_client.get_object(
    # Bucket=bucket_name,
    # Key=object_name,
    # )
    
    if object_flag:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'Hello, Umair! Object specified does exists, Please find attached presigned url {}\n paramters '.format(response)
        }
        
    else:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'Hello, Umair! Object specified does not exists '.format(response)
        }
        