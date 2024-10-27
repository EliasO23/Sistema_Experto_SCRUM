from experta import *




# Definición del hecho Proyecto
class Sprint(Fact):
    # """Clase Proyecto con propiedades fijas"""
    # def __init__(self, nombre="", estado="en-proceso", fecha_inicio=""):
    #     self.nombre = nombre
    #     self.estado = estado
    #     self.fecha_inicio = fecha_inicio
    pass

# Definición del sistema experto con las reglas
class GestionProyectos(KnowledgeEngine):

    recomendaciones = []

    @Rule(Sprint(numero=1))
    def crear_tareas_sprint_1(self):
        mensaje = "Creando tareas para el Sprint 1..."
        self.recomendaciones.append(mensaje)

    @Rule(Sprint(numero=3))
    def crear_tareas_sprint_1(self):
        mensaje = "Creando tareas para el Sprint 3..."
        self.recomendaciones.append(mensaje)
    # Otras reglas...

    def obtener_recomendaciones(self):
        return self.recomendaciones


# Inicialización del motor de inferencia
def inicializar_motor():
    # Crear una instancia del motor de inferencia
    engine = GestionProyectos()
    # Reiniciar el motor para limpiar hechos anteriores
    engine.reset()
    
    engine.declare(Sprint(numero=3))

    engine.run()

    # Retornamos las recomendaciones generadas
    return engine.obtener_recomendaciones()

# Función para declarar un nuevo proyecto en el motor
# def declarar_proyecto(engine, nombre, estado, fecha_inicio):
#     # Declarar el proyecto
#     proyecto = Proyecto(nombre=nombre, estado=estado, fecha_inicio=fecha_inicio)

#     engine.declare(proyecto)
#     # Ejecutar las reglas
#     engine.run()

#     proyectos_creados.append({
#         'nombre': nombre,
#         'estado': estado,
#         'fecha_inicio': fecha_inicio
#     })

# def obtener_proyectos():
#     return proyectos_creados