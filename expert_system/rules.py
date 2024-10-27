# from experta import *

# class ProyectoScrum(Fact):
#     """Información sobre el proyecto Scrum."""
#     pass

# class ScrumExpert(KnowledgeEngine):
#     def __init__(self):
#         super().__init__()
#         self.resultados = []  # Lista para almacenar los mensajes de salida

#     @Rule(ProyectoScrum(product_owner=True, backlog=True, equipo=True))
#     def proyecto_listo(self):
#         self.resultados.append("El proyecto está listo para la fase de desarrollo.")

#     @Rule(ProyectoScrum(product_owner=False))
#     def sin_product_owner(self):
#         self.resultados.append("El proyecto necesita un Product Owner.")

#     @Rule(ProyectoScrum(backlog=False))
#     def sin_backlog(self):
#         self.resultados.append("El proyecto necesita un backlog definido.")

#     @Rule(ProyectoScrum(equipo=False))
#     def sin_equipo(self):
#         self.resultados.append("El proyecto necesita un equipo asignado.")
