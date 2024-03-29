from apihelper import getTokenAndTask
from apihelper import sendAnswer

from openai import OpenAI

import requests

schema = {
    "name" : "addUser",
    "description" : "Add User to the database",
    "parameters" : {
        "type" : "object",
        "properties": {
            "name" : {
                "type" : "string",
                "description" : "Name of the user to add"
            },
            "surname" : {
                "type" : "string",
                "description" : "Surname of the user to add"
            },
            "year" : {
                "type" : "number",
                "description" : "Year in which the user has been born"
            },
        }
    }
}

token, task_json = getTokenAndTask("functions", None, None)
if task_json != None:
    sendAnswer(token, schema)