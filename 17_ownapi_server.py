from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

@app.route('/ownapi', methods=['GET', 'POST'])
def ownapi_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        question = data["question"]
        client = OpenAI()
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages = [{"role" : "user", "content" : question}])
        answer = response.choices[0].message.content
        print(answer)
        result = {"reply": answer}
        return result, 200
    else:
        print("ERROR")
        return "", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)