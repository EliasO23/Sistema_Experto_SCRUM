from utils.db import db

class Tareas(db.Model):

    id_tarea = db.Column(db.Integer, primary_key=True)
    id_sprint = db.Column(db.Integer, db.ForeignKey('sprints.id_sprint'))
    nombre = db.Column(db.String(500), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'en proceso', 'completada'), default='pendiente')
    dificultad = db.Column(db.Enum('1', '2', '3'), nullable=False, default='1')

    def __init__(self, id_sprint, nombre, estado='pendiente', dificultad='1'):
        self.id_sprint = id_sprint
        self.nombre = nombre
        self.estado = estado
        self.dificultad = dificultad
