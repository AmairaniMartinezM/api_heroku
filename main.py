import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import hashlib
import datetime
from fastapi import Depends
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBearer
from fastapi.security import  HTTPBasicCredentials
from fastapi.security import HTTPAuthorizationCredentials


# Crea la base de datos
conn = sqlite3.connect("contactos.db")

app = fastapi.FastAPI()
securityBearer = HTTPBearer()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contacto(BaseModel):
    email : str
    nombre : str
    telefono : str

# Rutas para las operaciones CRUD

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    # TODO Inserta el contacto en la base de datos y responde con un mensaje
    c = conn.cursor()
    c.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (?, ?, ?)',
              (contacto.email, contacto.nombre, contacto.telefono))
    conn.commit()
    return contacto

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    # TODO Consulta todos los contactos de la base de datos y los envia en un JSON
    c = conn.cursor()
    c.execute('SELECT * FROM contactos;')
    response = []
    for row in c:
        contacto = {"email":row[0],"nombre":row[1], "telefono":row[2]}
        response.append(contacto)
    return response


@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    # Consulta el contacto por su email
    c = conn.cursor()
    c.execute('SELECT * FROM contactos WHERE email = ?', (email,))
    contacto = None
    for row in c:
        contacto = {"email":row[0],"nombre":row[1],"telefono":row[2]}
    return contacto


@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto."""
    # TODO Actualiza el contacto en la base de datos
    c = conn.cursor()
    c.execute('UPDATE contactos SET nombre = ?, telefono = ? WHERE email = ?',
              (contacto.nombre, contacto.telefono, email))
    conn.commit()
    return contacto


@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    # TODO Elimina el contacto de la base de datos
    c = conn.cursor()
    c.execute('DELETE FROM contactos WHERE email = ?', (email,))
    conn.commit()
    return {"mensaje":"Contacto eliminado"}

@app.get("/")
def autenticacion(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    """Autenticación"""
    token = credentials.credentials
    connx = sqlite3.connect("base.bd")
    c = connx.cursor()
    c.execute('SELECT token FROM usuarios WHERE token = ?', (token,))
    existe = c.fetchone()
    if existe is  None:
        raise fastapi.HTTPException(status_code=401, detail="No autorizado")
    else:
        c.execute('SELECT timestamp FROM usuarios WHERE token = ?',(token,))
        for row in c:
            hora_bd = row[0]

        hora_actual = datetime.datetime.now()
        hora_hash = hora_actual.strftime("%H:%M")

        if hora_bd != hora_hash:
            raise fastapi.HTTPException(status_code=430, detail="Token Caducado")
        else:
            return {"mensaje: Bienvenido"}
        
    
security = HTTPBasic()
@app.get("/token") # endpoint para obtener token
def validar_usuario(credentials: HTTPBasicCredentials = Depends(security)): 
    """Validación de usuario"""
    username = credentials.username # se obtiene el username
    password = credentials.password # se obtiene el password
    hashpassword = hashlib.sha256(password.encode()).hexdigest() # se hashea el password

    connx = sqlite3.connect("base.bd") # conecta a la base de datos
    c = connx.cursor() # crea un cursor

    hora_actual = datetime.datetime.now() # obtiene la hora actual
    hora_actual_formateada = hora_actual.strftime("%H:%M") # formatea la hora actual


    caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()=+-*/@#$%&!?' # caracteres para generar el token
    longitud = 8 # longitud del token
    token = '' # variable para almacenar el token
    for i in range(longitud): # ciclo para generar el token
        token += random.choice(caracteres) # se agrega un caracter aleatorio al token
        
    hashtoken = hashlib.sha256(token.encode()).hexdigest() # se hashea el token
    # actualiza el token y la hora en la base de datos
    c.execute('UPDATE usuarios SET token = ?, timestamp = ? WHERE correo = ? AND password = ?', (hashtoken, hora_actual_formateada, username, hashpassword))
    connx.commit() # ejecuta la actualizacion

    c.execute('SELECT token FROM usuarios WHERE correo = ? AND password = ?', (username, hashpassword)) 
    existe = c.fetchone()
    if existe is None: 
        raise fastapi.HTTPException(status_code=401, detail="No autorizado")
    else:
        token = existe[0]
        return {"token":token}

    
