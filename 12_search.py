from apihelper import sendAnswer
from apihelper import getTokenAndTask

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.chat_models.openai import ChatOpenAI
from langchain_core.documents import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct, Distance, VectorParams, CollectionDescription

import time
import requests
import uuid
import json

import os
from dotenv import load_dotenv

COLLECTION_NAME = "my_collection"

load_dotenv()
qdrant = QdrantClient(os.getenv("QDRANT_HOST"))
embeddings = OpenAIEmbeddings()

if qdrant.collection_exists(COLLECTION_NAME) == False:
    qdrant.create_collection(collection_name = COLLECTION_NAME, vectors_config=VectorParams(size=1536, distance=Distance.COSINE, on_disk=True))

collectionInfo = qdrant.get_collection(COLLECTION_NAME)
if collectionInfo.points_count == 0:
    data = {}
    documents = []
    data_request = requests.get("https://unknow.news/archiwum_aidevs.json")
    if data_request.status_code == 200:
        data = data_request.json()
      

        points = []
        for entry in data:
            document = Document(page_content=str(entry), metadata={"source" : COLLECTION_NAME, "content":entry, "uuid":str(uuid.uuid4())})
            print(document)
            print("=======")
            embedding = embeddings.embed_query(document.page_content)
            points.append(PointStruct(id = document.metadata["uuid"], vector = embedding, payload = document.metadata))
        qdrant.upsert(collection_name = COLLECTION_NAME, points = points)

token, task_json = getTokenAndTask("search", None, None)
if task_json != None:
    question = task_json["question"]
    print(question)
    print("=======")
    question_embedding = embeddings.embed_query(question)
    search_result = qdrant.search(
        collection_name=COLLECTION_NAME, 
        query_vector=question_embedding,
        limit=1)
    print(search_result)
    print("=======")
    result_url = search_result[0].payload["content"]["url"]
    print(result_url)
    print("=======")
    sendAnswer(token, result_url)
    