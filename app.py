from flask import Flask,render_template,request, session,jsonify 
import json
import random
from groq import Groq

app = Flask(__name__) #inicializa o site
client = Groq(api_key=("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")) #Lê a chave da API para funcionar a IA
app.secret_key = "session_test" #Configura uma chave de sessão para poder mudar,ler, interpretar a sessão e os cookies
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
#Função que lê um arquivo json(até mesmo se tiver com emoji) e procura pelo dicionario as respostas e retorna uma dessas respostas de forma aleatoria
def predefine(n):
    with open('intents.json','r',encoding='utf-8') as messagePredefine:
        parsed = json.load(messagePredefine)
        answer = parsed['intents'][n]['response']
    return random.choice(answer)
#Na rota do servidor 'get_response', recebe e manda informações
@app.route('/get_response',methods=["GET","POST"])
#função que cria as respostas por IA
def responsebot():
    #Faz a requisição do input do usuario
    data = request.get_json()
    user = data['response']
    #Inicialização da IA Groq
    chat_completion = client.chat.completions.create(
        messages=[
            #Determina como o sistema funcionará
            {
                "role":"system",
                "content":"Você é um atendente da org Furia e-sports e necessita responder tudo que o usuario te mandar de pergunta, conforme as informações que você sabe, entretanto caso seja uma pergunta fora do escopo FURIA responda com: 'Não posso te ajudar com tal informação, fui programado para passar informações da furia', observações o sentimento furia de estar furioso não está condizente neste contexto e não é necessario se apresentar você sera apresentado por uma função anterior a sua resposta"
            },
            #Determina as entradas do usuario
            {
                "role": "user",
                "content": user,
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    #recebe as mensagens da ia e retorna pelo caminho do servidor definido
    responsebot = chat_completion.choices[0].message.content
    return jsonify({"response": responsebot})

#Manda e recebe informações pelo caminho principal do servidor
@app.route('/', methods=["GET","POST"])
#Função que inicia a render das paginas
def home():
    session.clear()
    #Condicional que verifica se existe mensagens no servidor, caso seja falso inicia uma lista que recebe todas as mensagens do usuario
    if'mensagens' not in session:
        answer = predefine(0)
        session['mensagens'] = []
        #Se no servidor houve a utilização do metodo POST, coleta o valor do input, adiciona a lista e previne a atualização da pagina
    if request.method == 'POST':
        mensagens = request.form['entry']
        session['mensagens'].append(mensagens)
        session.modified = False
    return render_template('index.html',mensagens=session['mensagens'],bot=answer) 

if __name__ == "__main__":
    app.run(debug=True)