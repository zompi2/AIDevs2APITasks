import requests
import json
import os

from dotenv import load_dotenv

def parseResponse(response):
    if response.status_code == 200:
        print("Response: ", response.json())
        return response.json()
    else:
        print("Failed to get response: ", response.status_code())
    return None

def postRequest(address, json_data):
    json_string = json.dumps(json_data)
    print("Making POST request to: ", address, " with data: ", json_string)
    response = requests.post(address, data=json_string)
    return parseResponse(response)

def getRequest(address):
    print("Making GET request to: ", address)
    response = requests.get(address)
    return parseResponse(response)

def getToken(test_name):
    load_dotenv()
    token_json_request = {"apikey" : os.getenv("AIDEVS_TOKEN")}
    json_response = postRequest("https://tasks.aidevs.pl/token/"+test_name, token_json_request)
    if json_response != None:
        if json_response["code"] == 0 and json_response["msg"] == "OK":
            return json_response["token"]
    return ""

def getTask(token):
    if token != "":
        json_response = getRequest("https://tasks.aidevs.pl/task/"+token)
        return json_response
    return None

def getTokenAndTask(test_name):
    token = getToken(test_name)
    task = getTask(token)
    return token, task

def sendAnswer(token, answer):
    json_answer = {"answer" : answer}
    json_response = postRequest("https://tasks.aidevs.pl/answer/"+token, json_answer)
    if json_response != None:
        if json_response["code"] == 0 and json_response["msg"] == "OK" and json_response["note"] == "CORRECT":
            return True
    return False

