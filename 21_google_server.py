from flask import Flask, request
from serpapi import GoogleSearch

from langchain.schema import SystemMessage
from langchain.schema import HumanMessage
from langchain.chat_models.openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("SERP_API_KEY")

app = Flask(__name__)

system_template = """Na podstawie zadanego pytania stwórz proste zapytanie dla wyszukiwarki internetowej, które będzie potem użyte w celu znalezienia odpowiedzi na zadane pytanie"""

@app.route('/google', methods=['GET', 'POST'])
def ownapi_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        question = data["question"]
        print(question)
        print("=====")
        chat = ChatOpenAI()
        resp = chat.invoke([
            SystemMessage(system_template),
            HumanMessage(question)
        ])
        ask = resp.content
        print(ask)
        print("===")
        search = GoogleSearch({
            "engine": "google",
            "q": ask,
            "api_key": key,
            "num":1
        })
        results = search.get_dict()
        organic_results = results["organic_results"]
        link = organic_results[0]["link"]
        print(link)
        print("===")
        result = {"reply": link}
        return result, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

