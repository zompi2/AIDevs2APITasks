from apihelper import getTokenAndTask
from apihelper import sendAnswer

from openai import OpenAI

import requests

token, task_json = getTokenAndTask("rodo", None, None)
if task_json != None:
    message = """Tell me something aobut yourself, but follow the given rules:
    - don't tell me your name, use %imie% insntead
    - don't tell me your family name, use %nazwisko%" instead
    - in a place of your job description insert %zawod% placeholder
    - don't tell me where you live, use %miasto% instead"""
    sendAnswer(token, message)