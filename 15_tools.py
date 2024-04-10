from apihelper import sendAnswer
from apihelper import getTokenAndTask

from langchain.schema import SystemMessage
from langchain.schema import HumanMessage
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models.openai import ChatOpenAI

import requests
import json

celect_tool_schema =  {
    "name" : "selectTool",
    "description" : "Wybierz odpowiednie narzędzie do zapisania danego przez użytkownika zadania",
    "parameters" : {
        "type" : "object",
        "properties": {
            "tool" : {
                "type" : "string",
                "description" : """Narzędzie które moze być użyte do wykonania tego zadania.: 
                TODO - jeżeli w zadaniu nie ma określonej daty lub czasu
                Calendar - jeżeli w zadaniu została zdefiniowana datas lub czas
                Możesz zwrócić tylko TODO albo Calendar, nic więcej
                examples####
                Q: Muszę kupić mleko
                A: TODO
                Q: Muszę pójść do dentysty jutro
                A: Calendar
                Q: Muszę zapisać się na kurs
                A: TODO
                Q: Muszę odwiedzić dentystę 5 marca
                A: Calendar
                """
            }
        }
    }
}

token, task_json = getTokenAndTask("tools", None, None)
if task_json != None:
    question = task_json["question"]
    print(question)
    chat_toolselect = ChatOpenAI(model_name="gpt-4").bind_functions([celect_tool_schema])
    chat_parser = ChatOpenAI(model_name="gpt-3.5-turbo")
    response = chat_toolselect.invoke(question)
    if len(response.additional_kwargs) > 0:
        json_call = json.loads(response.additional_kwargs["function_call"]["arguments"])
        answer = {"tool"}
        if json_call["tool"] == "Calendar":
            print("Calendar")
            prompt = ChatPromptTemplate.from_messages([
                    ("system", """Przekonwertuj zapytanie na krótką notkę do zapisania w kalendarzu. 
                                    W treści notki nie podawaj daty.
                                    Odpowiedź zwróć w formie Notka|Data. 
                                    Dla daty użyj formatu YYYY-MM-DD
                                    ### examples
                                    Q: Jutro muszę isć do dentysty
                                    A: Wizyta u dentysty|2024-04-11
                                    Q: 8 maja są urodziny Andrzeja
                                    A: Urodziny Andrzeja|2024-05-08
                                    ### context
                                    Dzisiaj jest środa, 2024-04-10)"""),
                    ("human", "{in_question}")])
            formatted_prompt = prompt.format_messages(in_question=question)
            calendar_response = chat_parser.invoke(formatted_prompt)
            print(calendar_response.content)
            split_response = calendar_response.content.split("|")
            answer_json = {"tool":"Calendar"}
            answer_json["desc"] = split_response[0]
            answer_json["date"] = split_response[1]
            answer = str(answer_json)

        elif json_call["tool"] == "TODO":
            print("TODO")
            prompt = ChatPromptTemplate.from_messages([
                    ("system", "Przekonwertuj zapytanie na krótkie polecenie dla listy TODO"),
                    ("human", "{in_question}")])
            formatted_prompt = prompt.format_messages(in_question=question)
            todo_response = chat_parser.invoke(formatted_prompt)
            print(todo_response.content)
            answer_json = {"tool":"ToDo"}
            answer_json["desc"] = todo_response.content
            answer = str(answer_json)
        else:
            print("Unknown Tool")
    
    if answer_json != "":
        sendAnswer(token, answer_json)