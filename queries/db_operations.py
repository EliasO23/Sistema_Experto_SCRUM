from utils.db import db

def buscar_por_palabra_clave(palabra_clave):
    """
    Busca tareas en la base de datos que contengan una palabra clave en el nombre.
    
    :param palabra_clave: Palabra clave a buscar.
    :return: Lista de resultados que coinciden con la palabra clave.
    """
    query = f"SELECT s.nombre, s.duracion FROM sprints_bc AS s WHERE s.identificador LIKE '%{palabra_clave}%';"
    
    resultados = db.session.execute(query).fetchall()
    return resultados

def insertar_en_sprint(id_proyecto, nombre, duracion):
    """
    Inserta una entrada en la tabla sprint con los datos proporcionados.
    
    :param id_proyecto: ID del proyecto (relacionado con la tarea).
    :param nombre: Nombre de la tarea.
    :param estado: Estado del sprint, por defecto 'activo'.
    """
    query = "INSERT INTO sprint (id_proyecto, nombre, duracion, estado) VALUES (:id_proyecto, :nombre, :duracion)"
    db.session.execute(query, {'id_proyecto': id_proyecto, 'nombre': nombre, 'duracion':duracion})
    db.session.commit()


