from apihelper import getTokenAndTask
from apihelper import sendAnswer

from openai import OpenAI

token, task_json = getTokenAndTask("moderation")
if task_json != None:
    if task_json["code"] == 0:
        client = OpenAI()
        tests = task_json["input"]
        responses = []
        for test in tests:
            response = client.moderations.create(input=test, model="text-moderation-latest")
            if response.results[0].flagged == True:
                responses.append(1)
            else:
                responses.append(0)
        result = sendAnswer(token, responses)
        if result == True:
            print("Taks COMPLETE!")
        else:
            print("Task FAILED!")