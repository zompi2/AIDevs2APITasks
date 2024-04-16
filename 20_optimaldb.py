from apihelper import sendAnswer
from apihelper import getTokenAndTask

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("RENDERFORM_API_KEY")

token, task = getTokenAndTask("optimaldb", None, None)
if task != None:
    with open("friends_compressed.json", 'r', encoding='utf-8') as file:
        json_string = file.read()
        sendAnswer(token, json_string)