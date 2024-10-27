from app import app
from utils.db import db

db.init_app(app)
with app.app_context(): #app = variable
    db.create_all() #Para ejecutar todo lo de la BD, para el CRUD


if __name__ == '__main__':
    app.run(debug=True)