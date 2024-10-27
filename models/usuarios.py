from utils.db import db

class Usuarios(db.Model):

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre, email, contraseña) -> None:  
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña