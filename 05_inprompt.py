from apihelper import getTokenAndTask
from apihelper import sendAnswer

from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import LLMChain

from langchain.schema import SystemMessage
from langchain.schema import HumanMessage

import requests
import json
import os

token, task_json = getTokenAndTask("inprompt", None, None)
if task_json != None:
    question = task_json["question"]
    input = task_json["input"]

    chat = ChatOpenAI()
    response = chat.invoke([SystemMessage("In one word in the nominative case tell the name of who this text concerns"), HumanMessage(question)])
    name = response.content
    print(name)

    properlines = []
    for line in input:
        if line.find(name) != -1:
            print(line)
            properlines.append(line)

    thiscontext = ""
    for properline in properlines:
        thiscontext+=properline
        thiscontext+="\n"

    print("-----")

    print(thiscontext)

    system_context = """With the given context answer to the given question.

        context###{context}###
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_context),
        ("human", "{in_question}")])

    formatted_prompt = prompt.format_messages(context=thiscontext, in_question=question)
    print(formatted_prompt)

    final_response = chat.invoke(formatted_prompt)
    print(final_response.content)

    sendAnswer(token, final_response.content)
