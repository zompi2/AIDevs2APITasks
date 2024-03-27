from apihelper import getTokenAndTask
from apihelper import sendAnswer

from openai import OpenAI

token, task_json = getTokenAndTask("embedding", None, None)
if task_json != None:
    client = OpenAI()
    response = client.embeddings.create(
        input="Hawaiian pizza",
        model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    if len(embedding) == 1536:
        sendAnswer(token, embedding)
