from apihelper import getTokenAndTask
from apihelper import sendAnswer

from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import LLMChain

from langchain.schema import SystemMessage
from langchain.schema import HumanMessage

import requests
import time

token, task_json = getTokenAndTask("scraper", None, None)
if task_json != None:
    got_result = False
    info = ""
    wait_time = 1
    while got_result == False:
        response = requests.get(task_json["input"], timeout=50, headers={'User-Agent' : """Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"""})
        if response.status_code == 200:
            info = response.content
            got_result = True
        else:
            print("error: " + str(response.content) + " waiting  " + str(wait_time) + " seconds")
            time.sleep(wait_time)
            wait_time=wait_time+1

    print(info)

    system_context = """With the given context answer to the given question. 
    Make sure the answer is no longer than 200 characters.
    The answer must be in Polish.
        ```context:
        {context}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_context),
        ("human", "{in_question}")])

    formatted_prompt = prompt.format_messages(context=info, in_question=task_json["question"])
    print(formatted_prompt)

    chat = ChatOpenAI()
    final_response = chat.invoke(formatted_prompt)
    answer = final_response.content
    print(answer)

    sendAnswer(token, answer)