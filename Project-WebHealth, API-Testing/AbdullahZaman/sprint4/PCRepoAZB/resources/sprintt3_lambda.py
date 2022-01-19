import boto3
import json
import logging
from custom_encoder import CustomEncoder


logger = logging.getLogger()    #It logs messages that we want to see
logger.setLevel(logging.INFO)   # Sets the threshold for this logger. Logs a message with level INFO on the root logger

dynamodbTableName = 'AbdullahSprint3'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthPath = '/health'
urlPath = '/url'
urlsPath = '/urls'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == urlPath:
        response = getItem(event['queryStringParameters']['URL_ADDRESS'])
    elif httpMethod == getMethod and path == urlsPath:
        response = getItems()
    elif httpMethod == postMethod and path == urlPath:
        response = saveItem(json.loads(event['body']))
    elif httpMethod == patchMethod and path == urlPath:
        requestBody = json.loads(event['body'])
        response = modifyItem(requestBody['URL_ADDRESS'],requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == urlPath:
        requestBody = json.loads(event['body'])
        response = deleteItem(requestBody['URL_ADDRESS'])
    else:
        response = buildResponse(404, 'Not Found')
    
    return response


def getItem(URL_ADDRESS):
    try:
        response = table.get_item(
                Key={
                    'URL_ADDRESS': URL_ADDRESS
                }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'URL_ADDRESS: %s not found' % URL_ADDRESS})
    except:
        logger.exception('Sprint3 getItem() Exception')
            
def getItems():
    try:
        response = table.scan()
        result = response['Items']
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Item'])
        
        body = result
        return buildResponse(200, body)
    
    except:
        logger.exception('Sprint3 getItems() Exception')
        
def saveItem(requestBody):
    table.put_item(Item=requestBody)
    try:
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('Sprint3 saveItem() Exception')

def modifyItem(URL_ADDRESS, updateValue):
    try:
        table.put_item(Item={"URL_ADDRESS": updateValue})
        response = table.delete_item(
                    Key={
                        'URL_ADDRESS': URL_ADDRESS
                    },
                    ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Sprint3 modifyItem() Exception')
        
def deleteItem(URL_ADDRESS):
    try:
        response = table.delete_item(
                    Key={
                        'URL_ADDRESS': URL_ADDRESS
                    },
                    ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Sprint3 modifyItem() Exception')


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response