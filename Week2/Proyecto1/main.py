from flask import Flask, render_template, request, jsonify
from chatbot import buscar_recetas, documentos_recetas
import os

# Inicializar la aplicación Flask
app = Flask(__name__)

# Definir la ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar la búsqueda de recetas
@app.route('/buscar_recetas', methods=['POST'])
def buscar():
    ingredientes = request.json.get('ingredientes', [])
    recetas = buscar_recetas(ingredientes, documentos_recetas)
    
    if recetas:
        return jsonify({"status": "success", "recetas": recetas})
    else:
        return jsonify({"status": "no_recipes_found", "recetas": []})

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
