from flask import Flask
from routes.views import views_blueprint

app = Flask(__name__)

# Configuración de conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://root:1234@localhost/scrum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'e5f02b7d8a4d4c8dbf5e8d6456fa1f94'


app.register_blueprint(views_blueprint)

