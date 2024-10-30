from utils.db import db


class SprintsBC(db.Model):

    id_sprint_bc = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    identificador = db.Column(db.String(100))

    def __init__(self, nombre, duracion, identificador):
        self.nombre = nombre
        self.duracion = duracion
        self.identificador = identificador
