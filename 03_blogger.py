from apihelper import getTokenAndTask
from apihelper import sendAnswer

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.chat_models.openai import ChatOpenAI

system_template = """You are a blog writer. 
    You will receive titles in every next message. 
    Write blog chapters based on those titles.
    Blog is about making pizza. 
    Write everything in Polish. 
    Every chapter shouldn't be longer than 1000 characters.
    ----------------
    """

system_message = SystemMessage(content=system_template)
human_message = HumanMessagePromptTemplate.from_template("{history} {input}")
chat_prompt = ChatPromptTemplate(messages=[system_message, human_message])

token, task_json = getTokenAndTask("blogger")
if task_json != None:
    if task_json["code"] == 0:
        parts = task_json["blog"]
        chat = ChatOpenAI()
        memory = ConversationBufferMemory()
        conversation = ConversationChain(llm=chat, verbose=True, memory=memory, prompt=chat_prompt)
        resps = []
        for part in parts:
            resps.append(conversation.run(part))
        result = sendAnswer(token, resps)
        if result == True:
            print("Taks COMPLETE!")
        else:
            print("Task FAILED!")