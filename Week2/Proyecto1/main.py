from flask import Flask, render_template, request, redirect, url_for, jsonify
from init_langchain import main
# Inicializar la aplicación Flask
app = Flask(__name__)


# Definir la ruta principal
@app.route('/',methods=['GET', 'POST'])
def index():
    query = None
    response = None

    if request.method == 'POST':
        query = request.form['query']
        response = main(query)  # Llama a la función que genera la respuesta del bot

    return render_template('index.html', query=query, response=response)
   












# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)