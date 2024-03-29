from apihelper import getTokenAndTask
from apihelper import sendAnswer

from openai import OpenAI

import requests

token, task_json = getTokenAndTask("whisper", None, None)
if task_json != None:
    response = requests.get("https://tasks.aidevs.pl/data/mateusz.mp3")
    if response.status_code == 200:
        with open("mateusz.mp3", 'wb') as audio_file:
            audio_file.write(response.content)
        with open("mateusz.mp3", 'rb') as audio_file:
            client = OpenAI()
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            sendAnswer(token, transcription.text)