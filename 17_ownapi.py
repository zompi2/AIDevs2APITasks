from apihelper import sendAnswer
from apihelper import getTokenAndTask

token, task = getTokenAndTask("ownapi", None, None)
if task != None:
    sendAnswer(token, "https://zompiapi.bieda.it/ownapi")