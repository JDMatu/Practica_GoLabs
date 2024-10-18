from flask import Flask, render_template, request, redirect, url_for, jsonify

# Inicializar la aplicación Flask
app = Flask(__name__)


# Definir la ruta principal
@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
@app.route('/routeYD')
def test():
    lblSaludo='<h1> Hi...! </h1>'
    return lblSaludo
=======
@app.route('/calle')
def calle():
    return '<h1> calle.com </h1>'
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636

@app.route('/hola')
def hola():
    return ("hola")










# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)