from utils.db import db

class Asignacion(db.Model):

    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_tarea = db.Column(db.Integer, db.ForeignKey('tareas.id_tarea'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))

    def __init__(self, id_tarea, id_usuario):
        self.id_tarea = id_tarea
        self.id_usuario = id_usuario
