from experta import *
from models.tareas import Tareas
from models.tareas_bc import TareasBC
from models.tareas_sprint import TareasSprint
from utils.db import db
from models.sprints_bc import SprintsBC
from models.sprints import Sprints
from sqlalchemy import text


# Definición del hecho Proyecto
class Sprint(Fact):
    id_sprint = Field(int, mandatory=True)
    id_proyecto = Field(int, mandatory=True)

class Proyecto(Fact):
    id_proyecto = Field(int, mandatory=True)
    requisitos = Field(str, mandatory=True)

# Definición del sistema experto con las reglas
class GestionProyectos(KnowledgeEngine):

    # Regla para agregar sprint de inicio por defecto
    @Rule(Proyecto(id_proyecto=MATCH.id_proyecto))
    def agregar_sprint_inicio(self, id_proyecto):
        print("Iniciando búsqueda en la base de datos para el sprint 'inicio'...")
        
        # Buscar el sprint en sprints_bc para el identificador "inicio"
        resultados = buscar_por_palabra_clave('inicio')
        
        # Agregar los resultados a Sprints
        agregar_sprints(resultados, id_proyecto)
        print("Sprint de 'inicio' agregado correctamente.")

    @Rule(Sprint(id_sprint=MATCH.id_sprint, id_proyecto=MATCH.id_proyecto))
    def crear_tareas_desde_sprint(self, id_sprint, id_proyecto):
        # Obtener el sprint seleccionado en la tabla `sprints` por ID
        sprint = Sprints.query.filter_by(id_sprint=id_sprint).first()

        if sprint:
            # Buscar el `sprint_bc` en la tabla `sprints_bc` usando el nombre del sprint seleccionado
            sprint_bc = SprintsBC.query.filter_by(nombre=sprint.nombre).first()
            
            if sprint_bc:
                # Buscar todas las tareas relacionadas con el sprint en `tareas_bc`
                tareas_relacionadas = (db.session.query(TareasBC)
                    .join(TareasSprint, TareasBC.id_tarea_bc == TareasSprint.id_tarea_bc)
                    .filter(TareasSprint.id_sprint_bc == sprint_bc.id_sprint_bc)
                    .all())

                # Insertar solo las tareas que no existan en la tabla `tareas` para el sprint y proyecto
                for tarea in tareas_relacionadas:
                    # Verificar si la tarea ya existe en la tabla `tareas` para el sprint
                    tarea_existente = Tareas.query.filter_by(
                        id_sprint=id_sprint,
                        nombre=tarea.nombre
                    ).first()
                    
                    if not tarea_existente:
                        nueva_tarea = Tareas(
                            id_sprint=id_sprint,
                            nombre=tarea.nombre,
                            dificultad=tarea.dificultad,
                            estado="pendiente"
                        )
                        db.session.add(nueva_tarea)

                # Confirmar la inserción de las tareas en la base de datos
                db.session.commit()
                print(f"Tareas del sprint '{sprint_bc.nombre}' creadas para el proyecto {id_proyecto}.")
            
            else:
                print(f"No se encontró un sprint en la base de conocimiento con el nombre '{sprint.nombre}'.")
            
        else:
            print(f"No se encontró el sprint en la base de conocimiento para ID: {id_sprint}.")

    @Rule(Proyecto(requisitos=MATCH.requisitos & CONTAINS('login'), id_proyecto=MATCH.id_proyecto))
    def generar_sprint_login(self, requisitos, id_proyecto):
        print("Iniciando búsqueda en la base de datos...")

        # Buscar los sprints en sprints_bc 
        resultados = buscar_por_palabra_clave('login')

        # Agregar los resultados a Sprints
        agregar_sprints(resultados, id_proyecto)

        print("Sprints agregados correctamente...")

    @Rule(Proyecto(requisitos=MATCH.requisitos & CONTAINS('gestion de productos'), id_proyecto=MATCH.id_proyecto))
    def generar_sprint_gestion_productos(self, requisitos, id_proyecto):
        print("Iniciando búsqueda en la base de datos...")

        # Buscar los sprints en sprints_bc 
        resultados = buscar_por_palabra_clave('gestion de productos')

        # Agregar los resultados a Sprints
        agregar_sprints(resultados, id_proyecto)

        print("Sprints agregados correctamente...")

    @Rule(Proyecto(requisitos=MATCH.requisitos & CONTAINS('reporte'), id_proyecto=MATCH.id_proyecto))
    def generar_sprint_reporte(self, requisitos, id_proyecto):
        print("Iniciando búsqueda en la base de datos...")

        # Buscar los sprints en sprints_bc 
        resultados = buscar_por_palabra_clave('reporte')

        # Agregar los resultados a Sprints
        agregar_sprints(resultados, id_proyecto)

        print("Sprints agregados correctamente...")

    @Rule(Proyecto(requisitos=MATCH.requisitos & CONTAINS('proveedores'), id_proyecto=MATCH.id_proyecto))
    def generar_sprint_proveedores(self, requisitos, id_proyecto):
        print("Iniciando búsqueda en la base de datos...")

        # Buscar los sprints en sprints_bc 
        resultados = buscar_por_palabra_clave('proveedores')

        # Agregar los resultados a Sprints
        agregar_sprints(resultados, id_proyecto)

        print("Sprints agregados correctamente...")

    # Regla para agregar sprint de final por defecto
    @Rule(Proyecto(id_proyecto=MATCH.id_proyecto))
    def agregar_sprint_final(self, id_proyecto):
        print("Iniciando búsqueda en la base de datos para el sprint 'final'...")
        
        # Buscar el sprint en sprints_bc para el identificador "final"
        resultados = buscar_por_palabra_clave('final')
        
        # Agregar los resultados a Sprints
        agregar_sprints(resultados, id_proyecto)
        print("Sprint de 'final' agregado correctamente.")


# Funciones
def ejecutar_motor_requisitos(id_proyecto, requisitos):
    sistema = GestionProyectos()
    sistema.reset()
    sistema.declare(Proyecto(id_proyecto=int(id_proyecto), requisitos=requisitos))
    print(id_proyecto)
    sistema.run()

def ejecutar_motor_tareas(id_sprint, id_proyecto):
    sistema = GestionProyectos()
    sistema.reset()
    sistema.declare(Sprint(id_sprint=int(id_sprint), id_proyecto=int(id_proyecto)))
    sistema.run()


def buscar_por_palabra_clave(palabra_clave):
    query = text(f"SELECT s.id_sprint_bc, s.nombre, s.duracion FROM sprints_bc AS s WHERE s.identificador LIKE '%{palabra_clave}%'")
    print(f"Ejecutando consulta en la base de datos: {query}")
    resultados = db.session.execute(query).fetchall()

    return resultados

def agregar_sprints(resultados, id_proyecto):
    # Verificar si se encontraron resultados
        if resultados:
            print(f"Se encontraron {len(resultados)} resultados en 'sprints_bc")
            for resultado in resultados:
                id_sprint_bc, nombre, duracion = resultado  
                
                # Verificar si el sprint ya existe en la base de datos para el proyecto actual
                sprint_existente = Sprints.query.filter_by(id_proyecto=id_proyecto, nombre=nombre).first()
                if sprint_existente:
                    print(f"Sprint '{nombre}' ya existe para el proyecto con ID {id_proyecto}. No se creará de nuevo.")
                    continue  # Saltar la creación si ya existe

                # Crear el sprint si no existe
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
          