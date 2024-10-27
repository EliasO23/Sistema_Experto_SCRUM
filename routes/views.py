from flask import Blueprint, flash, jsonify, redirect, request, render_template, session, url_for
from expert_system.motor_inferencia import inicializar_motor
from models.usuarios import Usuarios
from utils.db import db
from werkzeug.security import check_password_hash


views_blueprint = Blueprint('views', __name__)

# Ruta principal
@views_blueprint.route('/')
def index():
    return render_template('index.html')

@views_blueprint.route('/register')
def register():
    return render_template('register.html')

@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Consultar al usuario en la base de datos
        user = Usuarios.query.filter_by(email=email).first()

        if user and check_password_hash(user['password'], password):
            session['user'] = email
            print('Inicio de sesión exitoso')
            return redirect(url_for('main'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@views_blueprint.route('/agregar_usuarios')
def agregar_usuarios():
    usuario1 = Usuarios(nombre="Carlos Perez", email="carlos@example.com", contraseña="password123")
    usuario2 = Usuarios(nombre="Ana Lopez", email="ana@example.com", contraseña="password456")
    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.commit()
    return "Usuarios agregados correctamente"

@views_blueprint.route('/main')
def main():
    return render_template('main.html')

@views_blueprint.route('/new')
def new_project():
    return "New Project"

# Ruta para iniciar el motor de inferencia
@views_blueprint.route('/iniciar_motor', methods=['GET'])
def iniciar_motor():
    # Ejecutamos el motor de inferencia
    recomendaciones = inicializar_motor()
    
    # Devolvemos las recomendaciones como JSON para el frontend
    return jsonify(recomendaciones)



