from datetime import datetime
from flask import Blueprint, flash, jsonify, redirect, request, render_template, session, url_for
from expert_system.motor_inferencia import Proyecto, ejecutar_motor_asignaciones, ejecutar_motor_tareas
from models.asignacion import Asignacion
from models.equipo import Equipo
from models.proyectos import Proyectos
from models.sprints import Sprints
from models.tareas import Tareas
from models.usuarios import Usuarios
from utils.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from expert_system.motor_inferencia import GestionProyectos, ejecutar_motor_requisitos


views_blueprint = Blueprint('views', __name__)

# Ruta principal
@views_blueprint.route('/')
def index():
    return render_template('index.html')

# @views_blueprint.route('/register')
# def register():
#     return render_template('register.html')

@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Consultar al usuario en la base de datos
        user = Usuarios.query.filter_by(email=email).first()
        print(user)

        if user and check_password_hash(user.contraseña, password):
            session['user'] = user.id_usuario
            # flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('views.projects'))
        else:
            flash('Credenciales incorrectas', 'error')
            
    return render_template('login.html')

@views_blueprint.route('/insertar_proyecto')
def insertar_proyecto():
    # Crear una instancia del modelo Proyecto con datos estáticos
    proyecto_prueba = Proyectos(
        nombre="Proyecto de Prueba",
        descripcion="Este es un proyecto de prueba para verificar la inserción de datos.",
        requisitos="Login, Registro, Dashboard",
        estado="pendiente",
        fecha_inicio=datetime(2024, 10, 30),
        fecha_fin=datetime(2025, 1, 31)
    )
    # Insertar el proyecto en la base de datos
    db.session.add(proyecto_prueba)
    db.session.commit()
    
    return "Proyecto insertado con éxito"


@views_blueprint.route('/prueba', methods=['GET', 'POST'])
def prueba():
    if request.method == 'POST':
        requisitos = request.form.get('requisitos')

        if requisitos:
            requisitos = requisitos.lower()
            sistema = GestionProyectos()
            sistema.reset()

            sistema.declare(Proyecto(requisitos=requisitos))
            sistema.run()
        else:
            print("El campo 'requisitos' está vacío. Por favor ingresa un valor.", "danger")
        
    return render_template('prueba.html')

@views_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')  # Nueva entrada para confirmar la contraseña

        # Verificar si la contraseña coincide con la confirmación
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('register.html', nombre=nombre, email=email)

        # Encriptar la contraseña antes de guardarla en la base de datos
        hashed_password = generate_password_hash(password)
        
        # Crear el nuevo usuario y agregarlo a la base de datos
        nuevo_usuario = Usuarios(nombre=nombre, email=email, contraseña=hashed_password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('views.login'))
    
    return render_template('register.html')

@views_blueprint.route('/projects')
def projects():
    if 'user' in session:
        # Obtener los proyectos del usuario actual
        user_id = session['user']
        proyectos = Proyectos.query.filter_by(id_usuario=user_id).all()  # Filtrar proyectos por el usuario actual
        if not proyectos:
            flash('No hay proyectos disponibles para mostrar.', 'info')  # Mostrar mensaje si no hay proyectos
        return render_template('projects.html', show_navbar=True, proyectos=proyectos, has_project=False)  # Renderizar la página de proyectos con los proyectos del usuario

    return redirect(url_for('views.login'))


@views_blueprint.route('/projects/new_project', methods=['GET', 'POST'])
def new_project():

    if 'user' in session:
        # Verifica si el usuario está autenticado (si existe 'user' en la sesión)
        if request.method == 'POST':
            # Obtener los datos del formulario
            id_usuario = session['user']
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            requisitos = request.form.get('requisitos')
            estado = request.form.get('estado', 'pendiente')
            fecha_inicio = request.form.get('fecha_inicio')
            fecha_fin = request.form.get('fecha_fin')

            # Crear una instancia del modelo Proyectos
            nuevo_proyecto = Proyectos(
                id_usuario = id_usuario,
                nombre=nombre,
                descripcion=descripcion,
                requisitos=requisitos,
                estado=estado,
                fecha_inicio=fecha_inicio if fecha_inicio else None,
                fecha_fin=fecha_fin if fecha_fin else None
            )

            # Agregar y confirmar la transacción en la base de datos
            try:
                db.session.add(nuevo_proyecto)
                db.session.commit()
                flash('Proyecto creado exitosamente', 'success')
                return redirect(url_for('views.projects'))
            
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear el proyecto: {str(e)}', 'error')
            

        return render_template('projects/new_project.html', show_navbar=True) # Si el método es GET, renderiza la plantilla HTML para crear un nuevo proyecto
    return redirect(url_for('views.login')) # Si el usuario no está autenticado, redirige a la página de inicio de sesión


@views_blueprint.route('/projects/update_project/<int:id_proyecto>', methods=['GET', 'POST'])
def update_project(id_proyecto):
    # Obtiene el proyecto de la base de datos, si no lo encuentra, lanza un error 404
    proyecto = Proyectos.query.get_or_404(id_proyecto)

    if request.method == 'POST':
        # Actualiza los datos con la información del formulario
        proyecto.nombre = request.form['nombre']
        proyecto.descripcion = request.form['descripcion']
        proyecto.requisitos = request.form['requisitos']
        proyecto.fecha_inicio = request.form.get('fecha_inicio')
        proyecto.fecha_fin = request.form.get('fecha_fin')

        try:
            db.session.commit()  # Guarda los cambios en la base de datos
            flash('Proyecto actualizado con éxito', 'success')
            return redirect(url_for('views.projects'))
        except Exception as e:
            db.session.rollback()  # Revertir si hay un error
            flash(f'Error al actualizar el proyecto: {str(e)}', 'danger')

    return render_template('projects/update_project.html', show_navbar=True, proyecto=proyecto)

@views_blueprint.route('/main/<int:id_proyecto>')
def main(id_proyecto):
    if 'user' in session:
        proyecto = Proyectos.query.get(id_proyecto)

        requisitos = proyecto.requisitos.split(', ')

        usuarios = db.session.query(Usuarios, Equipo.rol_proyecto).\
        join(Equipo, Usuarios.id_usuario == Equipo.id_usuario).\
        filter(Equipo.id_proyecto == id_proyecto).all()

        sprints = Sprints.query.filter_by(id_proyecto=id_proyecto).all()


        return render_template('main.html', show_navbar=True, proyecto=proyecto, requisitos=requisitos, usuarios=usuarios, sprints=sprints, has_project=True)
    return redirect(url_for('views.login'))

@views_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('views.login'))



# # Ruta para iniciar el motor de inferencia
# @views_blueprint.route('/iniciar_motor', methods=['GET'])
# def iniciar_motor():
#     # Ejecutamos el motor de inferencia
#     recomendaciones = inicializar_motor()
    
#     # Devolvemos las recomendaciones como JSON para el frontend
#     return jsonify(recomendaciones)

@views_blueprint.route('/buscar_usuarios')
def buscar_usuarios():
    query = request.args.get('query')
    proyecto_id = request.args.get('proyecto_id')  # Asegúrate de pasar el ID del proyecto

    # Obtén los IDs de los usuarios que ya están en el equipo del proyecto
    usuarios_en_equipo = db.session.query(Equipo.id_usuario).filter(Equipo.id_proyecto == proyecto_id).all()
    ids_usuario_en_equipo = {usuario[0] for usuario in usuarios_en_equipo}  # Usamos un set para búsqueda rápida

    # Filtra los usuarios que no están en el equipo
    usuarios = Usuarios.query.filter(
        Usuarios.nombre.like(f'%{query}%'),
        Usuarios.id_usuario.notin_(ids_usuario_en_equipo)
    ).all()

    return jsonify([{'id_usuario': u.id_usuario, 'nombre': u.nombre} for u in usuarios])

@views_blueprint.route('/agregar_equipo', methods=['POST'])
def agregar_equipo():
    data = request.json
    proyecto_id = data['proyecto_id']
    users = data['users']
    
    for user in users:
        equipo = Equipo(
            id_proyecto=proyecto_id,
            id_usuario=user['id'],
            rol_proyecto=user['rol'],
            experiencia=user['experiencia']
        )
        db.session.add(equipo)
    
    db.session.commit()

    # Obtener la lista actualizada de usuarios
    usuarios = db.session.query(Usuarios.nombre, Equipo.rol_proyecto).join(Equipo).filter(Equipo.id_proyecto == proyecto_id).all()
    return jsonify({'message': 'Usuarios agregados al proyecto con éxito.', 'usuarios': [{'nombre': u[0], 'rol': u[1]} for u in usuarios]})

@views_blueprint.route('/eliminar_usuario_proyecto/<int:id_proyecto>/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario_proyecto(id_proyecto, id_usuario):
    equipo = db.session.query(Equipo).filter(Equipo.id_usuario == id_usuario, Equipo.id_proyecto == id_proyecto).first()
    
    if equipo:
        db.session.delete(equipo)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado del proyecto con éxito.'})
    
    return jsonify({'message': 'Usuario no encontrado en el proyecto.'}), 404


@views_blueprint.route('/sprints/<int:id_proyecto>', methods=['GET'])
def sprints(id_proyecto):
    if 'user' in session:
        proyecto = Proyectos.query.get(id_proyecto)
        sprints = Sprints.query.filter_by(id_proyecto=id_proyecto).all()  # Asegúrate de que tu modelo Sprints esté correctamente definido
        return render_template('sprints.html', proyecto=proyecto, sprints=sprints, show_navbar=True, has_project=True)
    return redirect(url_for('views.login'))  # Redirigir si no está autenticado


@views_blueprint.route('/sprints/update/<int:id_sprint>', methods=['POST'])
def update_sprint(id_sprint):
    if 'user' in session:
        sprint = Sprints.query.get(id_sprint)
        if sprint:
            # Obtener nuevas fechas del formulario
            sprint.fecha_inicio = request.form['fecha_inicio']
            sprint.fecha_fin = request.form['fecha_fin']

            # Guardar cambios en la base de datos
            db.session.commit()
            flash('Sprint actualizado correctamente.', 'success')
        else:
            flash('Sprint no encontrado.', 'danger')
    else:
        flash('Debes iniciar sesión para realizar esta acción.', 'danger')
    return redirect(url_for('views.sprints', id_proyecto=sprint.id_proyecto))


@views_blueprint.route('/crear_sprints/<int:id_proyecto>', methods=['POST'])
def crear_sprints(id_proyecto):
    if 'user' in session:

        print("Usuario en sesión, comenzando proceso para crear sprints...")  # Mensaje de depuración

        proyecto = Proyectos.query.get(id_proyecto)
        requisitos = proyecto.requisitos.lower()
        id = proyecto.id_proyecto

        print(f"Valor de requisitos: {requisitos}")

        ejecutar_motor_requisitos(id_proyecto, requisitos)
        print("Ejecución completa del motor de inferencia.") 

        return redirect(url_for('views.main', id_proyecto=id_proyecto))
    return redirect(url_for('views.login'))

@views_blueprint.route('/crear_tareas', methods=['POST'])
def crear_tareas():
    if 'user' in session:
        id_proyecto = request.form.get('id_proyecto')
        id_sprint = request.form.get('id_sprint')

        ejecutar_motor_tareas(id_sprint, id_proyecto)

        flash("Tareas creadas con éxito.")
        return redirect(url_for('views.main', id_proyecto=id_proyecto))
    return redirect(url_for('views.login'))

@views_blueprint.route('/proyecto/<int:id_proyecto>/sprint/<int:id_sprint>/tareas', methods=['GET'])
def get_tareas(id_proyecto, id_sprint):
    # Asegúrate de que el usuario esté autenticado
    if 'user' in session:
        # Filtrar tareas por id_proyecto e id_sprint, y obtener el nombre del usuario asignado si existe
        tareas = Tareas.query.join(Sprints, Tareas.id_sprint == Sprints.id_sprint) \
                             .outerjoin(Asignacion, Tareas.id_tarea == Asignacion.id_tarea) \
                             .outerjoin(Usuarios, Asignacion.id_usuario == Usuarios.id_usuario) \
                             .filter(Sprints.id_proyecto == id_proyecto, Tareas.id_sprint == id_sprint) \
                             .add_columns(Tareas.nombre, Tareas.estado, Tareas.dificultad, Usuarios.nombre.label("usuario_nombre")) \
                             .all()

        # Convertir las tareas en un formato JSON
        tareas_data = [
            {
                "nombre": tarea.nombre,
                "estado": tarea.estado,
                "dificultad": tarea.dificultad,
                "usuario_nombre": tarea.usuario_nombre or "No asignado"
            }
            for tarea in tareas
        ]
        
        return jsonify({"tareas": tareas_data})
    
    return jsonify({"error": "No autorizado"}), 401

@views_blueprint.route('/asignar_tareas', methods=['POST'])
def asignar_tareas():
    id_proyecto = request.form['id_proyecto']
    id_sprint = request.form['id_sprint']
    
    # Obtener las tareas del sprint seleccionado
    tareas = Tareas.query.filter_by(id_sprint=id_sprint, estado='pendiente').all()

    for tarea in tareas:
        print(f"Tarea ID: {tarea.id_tarea}, Nombre: {tarea.nombre}, Estado: {tarea.dificultad}")
    
    # Obtener los usuarios del equipo que pertenecen al proyecto y tienen rol de 'developer'
    usuarios = db.session.query(Usuarios.id_usuario, Equipo.experiencia, Equipo.rol_proyecto).\
        join(Equipo, Usuarios.id_usuario == Equipo.id_usuario).\
        filter(Equipo.id_proyecto == id_proyecto, Equipo.rol_proyecto == 'developer').all()
    
    for usuario in usuarios:
        print(f"Usuario ID: {usuario.id_usuario}, Experiencia: {usuario.experiencia}, Rol: {usuario.rol_proyecto}")
    
    ejecutar_motor_asignaciones(tareas, usuarios)

    print('motor')
    
    return redirect(url_for('views.main', id_proyecto=id_proyecto))