from apihelper import sendAnswer
from apihelper import getTokenAndTask
from openai import OpenAI

token, task = getTokenAndTask("md2html", None, None)
if task != None:
    input = task["input"]
    print(input)

    client = OpenAI()
    completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::9FdzmQ72",
        messages=[
            {"role": "system", "content": "Your goal is to convert MD to HTML. Be super concise, never add extra info from yourself."},
            {"role": "user", "content": input}
        ]
    )
    result = completion.choices[0].message.content
    print(result)

    sendAnswer(token, result)
