from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route("/borrar")
def borrar():
    return render_template('borrar.html')

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    return render_template('buscar.html')

@app.route("/editar")
def editar():
    return render_template('editar.html')

@app.route("/insertar")
def insertar():
    return render_template('insertar.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/prueba")
def prueba():
    return render_template('prueba.html')

@app.route("/ver")
def ver():
    return render_template('ver.html')

if __name__ == "__main__":
    app.run(debug=True)
