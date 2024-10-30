from utils.db import db

class Proyectos(db.Model):

    id_proyecto = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    requisitos = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum('pendiente', 'en_proceso', 'completado'), default='pendiente')
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)

    def __init__(self, id_usuario, nombre, descripcion, requisitos, estado='pendiente', fecha_inicio=None, fecha_fin=None):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.descripcion = descripcion
        self.requisitos = requisitos
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

