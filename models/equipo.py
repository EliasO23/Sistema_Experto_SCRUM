
from utils.db import db

class Equipo(db.Model):

    id_equipo = db.Column(db.Integer, primary_key=True)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id_proyecto'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    rol_proyecto = db.Column(db.Enum('admin', 'developer', 'product_owner', 'scrum_master'), nullable=False)
    experiencia = db.Column(db.Enum('senior', 'intermedio', 'junior'), nullable=False)

    def __init__(self, id_proyecto, id_usuario, rol_proyecto, experiencia):
        self.id_proyecto = id_proyecto
        self.id_usuario = id_usuario
        self.rol_proyecto = rol_proyecto
        self.experiencia = experiencia
