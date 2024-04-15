from apihelper import sendAnswer
from apihelper import getTokenAndTask

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("RENDERFORM_API_KEY")

token, task = getTokenAndTask("meme", None, None)
if task != None:
    image = task["image"]
    text = task["text"]

    response = requests.post("https://get.renderform.io/api/v2/render", headers={
        "X-API-Key" : key,
        "Content-Type" : "application/json" 
    }, json={
        "template" : "prickly-trouts-blink-slowly-1787",
        "data": {
            "image.src": image,
            "title.text": text
        }
    })

if response.status_code == 200:
    result_json = json.loads(response.content)
    href = result_json["href"]
    print(href)
    sendAnswer(token, href)
