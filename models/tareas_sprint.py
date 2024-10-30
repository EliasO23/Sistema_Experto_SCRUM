from utils.db import db

class TareasSprint(db.Model):

    id_tarea_sprint = db.Column(db.Integer, primary_key=True)
    id_sprint_bc = db.Column(db.Integer, db.ForeignKey('sprints_bc.id_sprint_bc'))
    id_tarea_bc = db.Column(db.Integer, db.ForeignKey('tareas_bc.id_tarea_bc'))

    def __init__(self, id_sprint_bc, id_tarea_bc):
        self.id_sprint_bc = id_sprint_bc
        self.id_tarea_bc = id_tarea_bc
