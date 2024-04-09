from apihelper import sendAnswer
from apihelper import getTokenAndTask

from langchain.schema import SystemMessage
from langchain.schema import HumanMessage
from langchain.chat_models.openai import ChatOpenAI

import requests
import json

schema_currency =  {
    "name" : "askCurrency",
    "description" : "Returns the question about currency exchange course",
    "parameters" : {
        "type" : "object",
        "properties": {
            "currency" : {
                "type" : "string",
                "description" : "the code of the currency"
            }
        }
    }
}

schema_population =  {
    "name" : "askPopulation",
    "description" : "Returns the question about country population",
    "parameters" : {
        "type" : "object",
        "properties": {
            "country" : {
                "type" : "string",
                "description" : "country name"
            }
        }
    }
}

schema_general =  {
    "name" : "askGeneral",
    "description" : "Returns the general question, not related to population or currency",
    "parameters" : {
        "type" : "object",
        "properties": {}
    }
}

def ask_population(conuntry_name):
    population_response = requests.get("https://restcountries.com/v3.1/all?fields=name,population")
    if population_response.status_code == 200:
        response_json = json.loads(population_response.content)
        for entry in response_json:
            if entry["name"]["common"] == conuntry_name:
                return entry["population"]

def ask_currency(currency_code):
    currency_response = requests.get("http://api.nbp.pl/api/exchangerates/tables/A")
    if currency_response.status_code == 200:
        test = json.loads(currency_response.text)
        rates = test[0]["rates"]
        for rate in rates:
            if rate["code"] == currency_code:
                return rate["mid"]

def ask_general(question):
    chat = ChatOpenAI()
    response = chat.invoke(question)
    return response.content

def parse_function_call(call):
    if call["name"] == "askCurrency":
        arguments = json.loads(call["arguments"])
        return ask_currency(arguments["currency"])
    elif call["name"] == "askPopulation":
        arguments = json.loads(call["arguments"])
        return ask_population(arguments["country"])
    elif call["name"] == "askGeneral":
        return ask_general(task_json["question"])
    return ""

token, task_json = getTokenAndTask("knowledge", None, None)
if task_json != None:
    print(task_json["question"])
    chat = ChatOpenAI(model_name="gpt-4").bind_functions([schema_currency, schema_population, schema_general])
    response = chat.invoke( [SystemMessage("""Do not answer to the question. When asked for a country use the english name of this country. EURO = EUR"""), 
                            HumanMessage(task_json["question"])])
    if len(response.additional_kwargs) > 0:
        call = response.additional_kwargs["function_call"]
        result = parse_function_call(call)
        print(result)
        sendAnswer(token, result)
