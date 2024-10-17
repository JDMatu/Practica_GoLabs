from flask import Flask, render_template, request, jsonify
from load_docs import query_recipes_from_db
from init_langchain import query_llm
import os

# Inicializar la aplicación Flask
app = Flask(__name__)

# Variable para almacenar la "memoria" de la conversación
conversation_memory = {
    "last_question": None,
    "last_response": None,
    "last_context": None
}

# Definir la ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar la búsqueda de recetas según ingredientes
@app.route('/buscar_recetas', methods=['POST'])
def buscar_recetas():
    ingredientes = request.json.get('ingredientes', [])
    
    # Buscar recetas en la base de datos
    recetas = query_recipes_from_db(ingredientes)
    
    if recetas:
        return jsonify({"status": "success", "recetas": recetas})
    else:
        return jsonify({"status": "no_recipes_found", "recetas": []})

# Ruta para procesar preguntas avanzadas (sustituciones, técnicas, etc.)
@app.route('/preguntar', methods=['POST'])
def preguntar():
    global conversation_memory
    pregunta = request.json.get('pregunta', '').lower()
    
    # Verificar si la pregunta es una afirmación basada en la conversación previa
    if pregunta in ['sí', 'si', 'claro', 'por favor', 'cuéntame más']:
        # Si el último contexto es sobre una receta de pizza, mostrar la receta completa
        if conversation_memory["last_context"] and "pizza margarita" in conversation_memory["last_context"].lower():
            # Llamar a la función para obtener la receta completa de la base de datos
            receta = obtener_receta("Pizza Margarita")
            return jsonify({
                "status": "success",
                "respuesta": f"Aquí tienes la receta completa para la Pizza Margarita:\n\nIngredientes:\n{receta['ingredientes']}\n\nProcedimiento:\n{receta['procedimiento']}"
            })
        else:
            return jsonify({
                "status": "error",
                "respuesta": "Lo siento, no tengo más información sobre eso."
            })
    
    # Utilizar el LLM para responder la nueva pregunta
    respuesta = query_llm(pregunta)
    
    # Guardar la pregunta, respuesta y contexto en la memoria
    conversation_memory["last_question"] = pregunta
    conversation_memory["last_response"] = respuesta
    conversation_memory["last_context"] = respuesta  # Se puede refinar para guardar un contexto más específico

    return jsonify({"status": "success", "respuesta": respuesta})

# Función para obtener una receta específica de la base de datos
def obtener_receta(nombre_receta):
    recetas = query_recipes_from_db([nombre_receta])
    if recetas:
        # Asumimos que hay una receta encontrada, devolver la primera
        return {
            "ingredientes": recetas[0].split("\n\n")[1],  # Parte de ingredientes
            "procedimiento": recetas[0].split("\n\n")[2]  # Parte de procedimiento
        }
    else:
        return {
            "ingredientes": "No se encontraron ingredientes.",
            "procedimiento": "No se encontró el procedimiento."
        }

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
