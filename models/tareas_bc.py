from utils.db import db

class TareasBC(db.Model):

    id_tarea_bc = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    dificultad = db.Column(db.Enum('1', '2', '3'), nullable=False, default='1')

    def __init__(self, nombre, dificultad='1'):
        self.nombre = nombre
        self.dificultad = dificultad
