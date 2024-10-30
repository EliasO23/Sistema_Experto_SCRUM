from utils.db import db

class Sprints(db.Model):

    id_sprint = db.Column(db.Integer, primary_key=True)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id_proyecto'))
    nombre = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.Enum('activo', 'completado', 'inactivo'), default='activo')

    def __init__(self, id_proyecto, nombre, fecha_inicio=None, fecha_fin=None, estado='activo'):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
