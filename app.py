from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route("/buscar",methods=["GET","POST"])
def buscar():
    return render_template('buscar.html')

@app.route("/prueba")
def prueba():
    return render_template('prueba.html')