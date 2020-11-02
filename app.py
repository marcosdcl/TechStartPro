import csv
from flask import Flask
from models import db, Category
from blueprints.views import products_blueprint

# app = Flask(__name__)
# app.config.from_object('settings')
# app.register_blueprint(products_blueprint)

def create_app(config_filename=None):
    app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)

    app.register_blueprint(products_blueprint)

    return app

def init_db(app):
    """ Initializes my database coming from models """
    db.init_app(app)
    db.app = app
    db.create_all()

    categories = Category.query.all()

    if categories:
        pass
    else:
        with open('categorias.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for collumn in reader:
                category = Category(name=collumn['nome'])
                db.session.add(category)
                db.session.commit()
