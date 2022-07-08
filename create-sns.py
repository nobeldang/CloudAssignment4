import boto3

sns = boto3.client("sns", region_name='us-east-1')

# create topic
topic_name = "SnsTopic"
create_res = sns.create_topic(Name=topic_name)
topic_arn = create_res.get("TopicArn")


email_sub = sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint="EMAIL_ID")