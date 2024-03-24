from apihelper import getTokenAndTask
from apihelper import sendAnswer

token, task_json = getTokenAndTask("helloapi")
if task_json != None:
    if task_json["code"] == 0:
        result = sendAnswer(token, task_json["cookie"])
        if result == True:
            print("Taks COMPLETE!")
        else:
            print("Task FAILED!")