from apihelper import sendAnswer
from apihelper import getTokenAndTask

from openai import OpenAI

token, task_json = getTokenAndTask("gnome", None, None)
if task_json != None:
    url = task_json["url"]
    api_message = {
        "role": "user",
        "content": [{
            "type": "text",
            "text": """I will give you a drawing of a gnome with a hat on his head. 
                        Tell me what is the color of the hat in POLISH. 
                        If there will be no gnome or hat in this drawing return "ERROR" as an answer"""
        },
        {
            "type": "image_url",
            "image_url": {
                "url": url,
            }
        }]
    }
    print(api_message)
    client = OpenAI()
    response = client.chat.completions.create(model="gpt-4-turbo", messages = [api_message], max_tokens=300)
    response_str = response.choices[0].message.content
    print(response_str)
    sendAnswer(token, response_str)