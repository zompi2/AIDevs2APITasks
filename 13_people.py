from apihelper import sendAnswer
from apihelper import getTokenAndTask

from langchain.schema import SystemMessage
from langchain.schema import HumanMessage

from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain.chat_models.openai import ChatOpenAI

import requests
import json

token, task_json = getTokenAndTask("people", None, None)
if task_json != None:
    chat = ChatOpenAI()

    question = task_json["question"]
    print(question)
    print("===")

    response_name = chat.invoke([
        SystemMessage("""
                      In form of JSON ["name" : name, "surname" : surname] answer who this question concerns? 
                      Use formal names only:
                      Kasia = Katarzyna
                      Krysia = Krystyna
                      Tomek = Tomasz
                      """), 
        HumanMessage(question)
        ])
    
    response_name_json = json.loads(response_name.content)
    print(response_name_json)
    print("===")

    data_request = requests.get("https://tasks.aidevs.pl/data/people.json")
    if data_request.status_code == 200:
        people_data = data_request.json()
        for person in people_data:
            if person["imie"] == response_name_json["name"] and person["nazwisko"] == response_name_json["surname"]:
                system_context = """With the given context answer to the given question.
                                    context###{context}###
                                    """
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_context),
                    ("human", "{in_question}")])

                formatted_prompt = prompt.format_messages(context=person, in_question=question)
                print(formatted_prompt)

                final_response = chat.invoke(formatted_prompt)
                print(final_response.content)
                sendAnswer(token, final_response.content)
                break
