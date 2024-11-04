from experta import *
from utils.db import db
from models.sprints_bc import SprintsBC
from models.sprints import Sprints
from sqlalchemy import text


# Definición del hecho Proyecto
class Sprint(Fact):
    # """Clase Proyecto con propiedades fijas"""
    # def __init__(self, nombre="", estado="en-proceso", fecha_inicio=""):
    #     self.nombre = nombre
    #     self.estado = estado
    #     self.fecha_inicio = fecha_inicio
    pass

class Proyecto(Fact):
    id_proyecto = Field(int, mandatory=True)
    requisitos = Field(str, mandatory=True)

# Definición del sistema experto con las reglas
class GestionProyectos(KnowledgeEngine):

    recomendaciones = []

    @Rule(Proyecto(requisitos=MATCH.requisitos & CONTAINS('login'), id_proyecto=MATCH.id_proyecto))
    def generar_sprints(self, requisitos, id_proyecto):
        print("Iniciando búsqueda en la base de datos...")

        # Buscar los sprints en sprints_bc 
        resultados = buscar_por_palabra_clave('login')

        # Agregar los resultados a Sprints
        agregar_sprints(resultados, id_proyecto)

        print("Sprints agregados correctamente...")

    @Rule(Sprint(numero=1))
    def crear_tareas_sprint_1(self):
        mensaje = "Creando tareas para el Sprint 1..."
        self.recomendaciones.append(mensaje)

    # Otras reglas...

    def obtener_recomendaciones(self):
        return self.recomendaciones


# Funciones
def ejecutar_motor_requisitos(id_proyecto, requisitos):
    sistema = GestionProyectos()
    sistema.reset()
    sistema.declare(Proyecto(id_proyecto=id_proyecto, requisitos=requisitos))
    sistema.run()


def buscar_por_palabra_clave(palabra_clave):
    query = text(f"SELECT s.id_sprint_bc, s.nombre, s.duracion FROM sprints_bc AS s WHERE s.identificador LIKE '%{palabra_clave}%'")
    print(f"Ejecutando consulta en la base de datos: {query}")
    resultados = db.session.execute(query).fetchall()

    return resultados

def agregar_sprints(resultados, id_proyecto):
    # Verificar si se encontraron resultados
        if resultados:
            print(f"Se encontraron {len(resultados)} resultados en 'sprints_bc' para el identificador 'login'.")
            for resultado in resultados:
                id_sprint_bc, nombre, duracion = resultado  # Ajuste para acceder a la tupla correctamente
                
                nuevo_sprint = Sprints(
                    id_proyecto=id_proyecto,  # ID del proyecto en el hecho
                    nombre=nombre,
                    estado='activo'
                )
                db.session.add(nuevo_sprint)
            
            db.session.commit()
            print("Sprints creados con éxito y almacenados en la base de datos.")
        else:
            print("No se encontraron resultados en la base de datos")
          