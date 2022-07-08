import boto3
import json
import requests



# Lambda execution starts here
def lambda_handler(event, context):
    region = "us-east-1" 
    service = "es"
    credentials = boto3.Session().get_credentials()
    sns = boto3.client('sns', region_name='us-east-1')
    curr_event = event['currentIntent']['slots']
    q = ""
    for i in curr_event.keys():
        q = curr_event[i]
    
    host = "HOST_NAME" 
    
    index = "posts"
    # # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    # q = event["queryStringParameters"]["q"]

    url = host + "/" + index + "/_search?"
    url = url + "q={q}".format(q = q)
    
    # Make the signed HTTP request
    r = requests.get(url, auth=("USERNAME","PASS"))
    
    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }
    
    idx = []
    res = json.loads(r.content.decode('utf-8'))
    for vals in res["hits"]["hits"]:
        idx.append(vals["_id"])
    
    if len(idx)==0:
        response['body'] = "No answers found for this category"
        return response
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('posts')
    
    result = []
    for val in idx:
        resp = table.get_item(Key = {"id": int(val)})
        if "Item" in resp.keys():
            result.append(resp["Item"][" posts"])
    
    if len(result)==0:
        # response['body'] = "No answers found for this category"
        sns.publish(TopicArn='SNS-ARN', Message=json.dumps(str(resp)))
        return  {
            "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "No answers found for this category"
            },
        }}
        
    if len(result)>=3:
        result = result[:3]
    print(len(result))
    resp = {}
    c = 0
    for i in result:
        idx = "Answer" + str(c) 
        resp[idx] = result[c]
        c = c + 1
    sns.publish(TopicArn='SNS-ARN', Message=json.dumps(str(resp)))
    
    #Add the search results to the response
    
    # response['body'] = str(result)
    # print(result)
    return  {
            "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Answer sent via email, please check email"
            },
        }}