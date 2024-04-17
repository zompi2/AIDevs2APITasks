from apihelper import sendAnswer
from apihelper import getTokenAndTask

token, task = getTokenAndTask("optimaldb", None, None)
if task != None:
    with open("friends_compressed.json", 'r', encoding='utf-8') as file:
        json_string = file.read()
        sendAnswer(token, json_string)