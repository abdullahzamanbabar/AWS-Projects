from resources import s3bucket
import boto3,os
#import json

def lambda_handler(event, context):
    URLs = s3bucket.read_file("abdullahzamanbucket", "urlsList.json") 
    client_ = boto3.client('dynamodb')
    #info = json.loads(info)
    
    for U in URLs:
        item = {
            'URL_ADDRESS': {'S': U}
                }
        client_.put_item(TableName="AZBsprint3", Item=item)