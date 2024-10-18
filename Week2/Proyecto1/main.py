from flask import Flask, render_template, request, redirect, url_for, jsonify

#Cargar la funcion que carga los documentos en la base de vectores
from load_docs import generate_data_store
from init_langchain import chat
from controlador_recetas import get_recipes, get_recipes_by_Ingredients, save_recipe


# Inicializar la aplicación Flask
app = Flask(__name__)


# Definir la ruta principal
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_receta')
def add_receta():
    return render_template('add_receta.html')


@app.route('/recetas')
def recetas():
    recetas = get_recipes()
    return render_template('recetas.html', recetas=recetas)


@app.route('/chat', methods=['POST'])
def chats():
    data = request.get_json()
    user_message = data.get('message', '')
    res = chat(user_message)
    print(res)
    return jsonify({'response': res})



@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save('static/data/' + file.filename)
        generate_data_store()
        return redirect(url_for('index'))
    

@app.route('/buscar_recetas', methods=['POST'])
def buscar_recetas():
    print("Buscando")
    data = request.get_json()
    ingredientes = data.get('ingredientes', [])
    
    # Buscar recetas en la base de datos
    recetas = get_recipes_by_Ingredients(ingredientes)
    print(recetas)
    
    if recetas:
        return jsonify({"status": "success", "recetas": recetas})
    else:
        return jsonify({"status": "no_recipes_found", "recetas": []})
    
@app.route('/saveRecipe', methods=['POST'])
def saveRecipe():
    nombre = request.form['titulo']
    ingredientes = request.form['ingredientes']
    preparacion = request.form['preparacion']
    save_recipe(nombre, ingredientes, preparacion)
    return redirect(url_for('add_receta'))













# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)