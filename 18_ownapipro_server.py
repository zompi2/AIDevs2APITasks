from flask import Flask, request

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.chat_models.openai import ChatOpenAI

system_template = """Answer to any question.
    Keep answers super concise. Answer in one sentence.
    If there is no question, remember the fact and answer "Ok, I will remember that.".
    Always answer correctly, according to your knowledge.
    #### example:
    Human: What is the capital of Poland?
    AI: Warsaw!
    Human: I'm living in Berlin
    AI: OK. Thx for the info.
    Human: Where am I living?
    AI: You are living in Berlin
    Human: My favourite number is 123
    AI: OK. Get it.
    Human: What's my favourite number?
    AI: It's 123
    ----------------
    """

system_message = SystemMessage(content=system_template)
human_message = HumanMessagePromptTemplate.from_template("{history} {input}")
chat_prompt = ChatPromptTemplate(messages=[system_message, human_message])
chat = ChatOpenAI(model="gpt-4")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=chat, verbose=False, memory=memory, prompt=chat_prompt)

app = Flask(__name__)

@app.route('/ownapipro', methods=['GET', 'POST'])
def ownapi_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        question = data["question"]
        print(question)
        print("=====")
        response = conversation.run(question)
        result = {"reply": response}
        print(result)
        print("=====")
        return result, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

