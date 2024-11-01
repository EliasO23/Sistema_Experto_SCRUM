from datetime import datetime
from flask import Blueprint, flash, jsonify, redirect, request, render_template, session, url_for
from expert_system.motor_inferencia import Proyecto, inicializar_motor
from models.proyectos import Proyectos
from models.usuarios import Usuarios
from utils.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from expert_system.motor_inferencia import GestionProyectos


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
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('views.projects'))
        else:
            flash('Credenciales incorrectas', 'danger')
            
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

@views_blueprint.route('/main')
def main():
    if 'user' in session:
        return render_template('main.html')
    return redirect(url_for('views.login'))

@views_blueprint.route('/projects')
def projects():
    if 'user' in session:
        # Obtener los proyectos del usuario actual
        user_id = session['user']
        proyectos = Proyectos.query.filter_by(id_usuario=user_id).all()  # Filtrar proyectos por el usuario actual
        if not proyectos:
            flash('No hay proyectos disponibles para mostrar.', 'info')  # Mostrar mensaje si no hay proyectos
        return render_template('projects.html', proyectos=proyectos)  # Renderizar la página de proyectos con los proyectos del usuario

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

            if requisitos:
                requisitos = requisitos.lower()
                sistema = GestionProyectos()
                sistema.reset()

                sistema.declare(Proyecto(requisitos=requisitos))
                sistema.run()
            else:
                print("El campo 'requisitos' está vacío. Por favor ingresa un valor.", "danger")
            

        return render_template('projects/new_project.html') # Si el método es GET, renderiza la plantilla HTML para crear un nuevo proyecto
    return redirect(url_for('views.login')) # Si el usuario no está autenticado, redirige a la página de inicio de sesión

@views_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('views.login'))

# Ruta para iniciar el motor de inferencia
@views_blueprint.route('/iniciar_motor', methods=['GET'])
def iniciar_motor():
    # Ejecutamos el motor de inferencia
    recomendaciones = inicializar_motor()
    
    # Devolvemos las recomendaciones como JSON para el frontend
    return jsonify(recomendaciones)



