from apihelper import sendAnswer
from apihelper import getToken
from apihelper import getTask

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.chat_models.openai import ChatOpenAI

import time

system_template = """The user will tell you a trivia about a famous person.
    You need to guess the name of that famous person.
    If you don't know the answer say NO.
    If you know the answer say YES.
    Answer truthfully to your knowledge and say YES only when you are sure the answer.
    Keep you answer super concise. Don't say anything more than one word.
    ----------------
    """

system_message = SystemMessage(content=system_template)
human_message = HumanMessagePromptTemplate.from_template("{history} {input}")
chat_prompt = ChatPromptTemplate(messages=[system_message, human_message])

chat = ChatOpenAI()
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=chat, verbose=True, memory=memory, prompt=chat_prompt)

is_done = False

token = getToken("whoami")

while is_done == False:
    task_json = getTask(token)
    if task_json != None and task_json["code"] == 0:
        response = conversation.run(task_json["hint"])
        if response == "YES":
            response = conversation.run("Who is it?")
            print(response)
            sendAnswer(token, response)
            is_done = True

      