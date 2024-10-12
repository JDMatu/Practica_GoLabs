from flask import Flask, request, jsonify, render_template, redirect, url_for
from chatbot import chatbot

app = Flask(__name__)

@app.route('/')
def home():
    idiomas = ['Inglés', 'Español', 'Chino', 'Hindi', 'Árabe', 'Portugués', 'Bengalí', 'Ruso', 'Japonés', 'Lahnda', 'Alemán', 'Coreano', 'Francés', 'Telugu', 'Maratí', 'Turco', 'Tamil', 'Vietnamita', 'Urdu', 'Italiano']
    return render_template('index.html', idiomas=idiomas)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # Obtiene el JSON enviado por el cliente
    user_message = data.get('message', '')  # Obtiene el mensaje del usuario
    inputLanguage = data.get('inputLanguage', 'Español')
    outputLanguage = data.get('outputLanguage', 'English')
    print(inputLanguage, outputLanguage, user_message)
    respuesta = chatbot(inputLanguage, outputLanguage, user_message)  # Obtiene la respuesta del chatbot
    return jsonify({'response': respuesta.content})

if __name__ == '__main__':
    app.run(debug=True)

