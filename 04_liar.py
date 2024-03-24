from apihelper import getTokenAndTask
from apihelper import sendAnswer

from langchain.prompts import PromptTemplate
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import LLMChain

import requests
import json
import os

token, task_json = getTokenAndTask("liar", None, {"question": "What is the highest mountain in the world?"})
if task_json != None:
    if task_json["code"] == 0:
        answer = task_json["answer"]
        print(answer)

        chat = ChatOpenAI()
        prompt = PromptTemplate.from_template("Return YES or NO if the prompt: {prompt} tells about Mount Everest or Mt. Everest")
        chain = LLMChain(llm=chat,prompt=prompt)
        result = chain.run(answer)
        print(result)

        sendAnswer(token, result)