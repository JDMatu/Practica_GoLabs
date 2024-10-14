from flask import Flask, render_template, request, redirect, url_for, jsonify

# Inicializar la aplicación Flask
app = Flask(__name__)


# Definir la ruta principal
@app.route('/')
def index():
    return render_template('index.html')













# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)