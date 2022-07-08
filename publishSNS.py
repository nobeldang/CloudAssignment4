import boto3
import json


sns = boto3.client('sns', region_name='us-east-1')

sns.publish(TopicArn='SNS-ARN',
            Message=json.dumps("Hello for SNS"))