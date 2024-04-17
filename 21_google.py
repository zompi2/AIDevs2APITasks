from apihelper import sendAnswer
from apihelper import getTokenAndTask

token, task = getTokenAndTask("google", None, None)
if task != None:
    sendAnswer(token, "https://zompiapi.bieda.it/google")