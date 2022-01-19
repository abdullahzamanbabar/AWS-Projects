import boto3
#import json

def lambda_handler(event, context):
    #write to dynamodb database
    #resource = boto3.resource('dynamodb') 
    client_ = boto3.client('dynamodb')
    info1 = event['Records'][0]['Sns']['MessageId']
    info2 = event['Records'][0]['Sns']['Timestamp']
    #info = json.loads(info)
    item = {
        'AlarmDetails': {'S': info1},
        'Timestamp' : {'S': info2}
            }
    client_.put_item(TableName="AbdullahTable", Item=item)