from utils.db import db
from sqlalchemy import text

def buscar_por_palabra_clave(palabra_clave):
    
    query = text(f"SELECT s.id_sprint_bc, s.nombre, s.duracion FROM sprints_bc AS s WHERE s.identificador LIKE '%{palabra_clave}%'")
    print(f"Ejecutando consulta en la base de datos: {query}")

    resultados = db.session.execute(query).fetchall()
    return resultados

def insertar_en_sprint(id_proyecto, nombre, duracion):
   
    print(f"Insertando datos en 'sprints': id_proyecto={id_proyecto}, nombre={nombre}, duracion={duracion}")
    query = "INSERT INTO sprints (id_proyecto, nombre, fecha_inicio, fecha_fin, estado) VALUES (:id_proyecto, :nombre, NOW(), DATE_ADD(NOW(), INTERVAL :duracion DAY), 'activo')"
    db.session.execute(query, {'id_proyecto': id_proyecto, 'nombre': nombre, 'duracion': duracion})
    db.session.commit()


