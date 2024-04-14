from apihelper import sendAnswer
from apihelper import getTokenAndTask

import requests

token, task = getTokenAndTask("ownapipro", None, None)
if task != None:
    sendAnswer(token, "https://zompiapi.bieda.it/ownapipro")