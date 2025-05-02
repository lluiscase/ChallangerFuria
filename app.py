from flask import Flask,render_template,request, session
from dotenv import load_dotenv
from groq import Groq
import json
import random


client = Groq(api_key="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")
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"

botmensagens = []

def predefine(n):
    with open('intents.json','r',encoding='utf-8') as messagePredefine:
        parsed = json.load(messagePredefine)
        answer = parsed['intents'][n]['response']
    return random.choice(answer)

@app.route('/', methods=["GET","POST"])
def home():
    session.clear()
    if'mensagens' not in session:
        answer = predefine(0)
        session['mensagens'] = []
    if request.method == 'POST':
        mensagens = request.form['entry']
        session['mensagens'].append(mensagens)
        session.modified = False
    return render_template('index.html',mensagens=session['mensagens'],bot=answer) 


if __name__ == "__main__":
    app.run(debug=True)