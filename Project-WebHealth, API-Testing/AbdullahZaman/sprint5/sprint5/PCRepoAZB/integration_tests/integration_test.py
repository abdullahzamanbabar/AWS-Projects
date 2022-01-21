import requests
import pytest
import os
import json

# Finding the unique ID of API Gateway. The API ID changes everytime the pipeline is deployed.
apis = json.load(os.popen('aws apigateway get-rest-apis'))  # popen runs the cli commands
apis = apis["items"]
for dic in apis:
    if dic["name"] == "AzbApisprint5":
        api_ID = dic["id"]
        break

# Creating the URL of the API Gateway
url = "https://"+api_ID+".execute-api.us-east-2.amazonaws.com/prod"
item = {"URL_ADDRESS": "www.test123.com"}
item1 = {
		"URL_ADDRESS": "www.test123.com",
		"updateValue": "www.test123456.com"
		}

def test_health():
    response = requests.get(url+"/health")
    statusCode = response.status_code
    assert statusCode == 200

def test_url_post():
    response = requests.post(url+"/url",json=item)
    statusCode = response.status_code
    assert statusCode == 200

def test_url_delete():
    response = requests.delete(url+"/url",json=item)
    statusCode = response.status_code
    assert statusCode == 200

def test_url_patch():
    requests.post(url+"/url",json=item)
    response = requests.patch(url+"/url",json=item1)
    statusCode = response.status_code
    assert statusCode == 200