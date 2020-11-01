from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

def init_db():
    """ Initializes my database coming from models """
    db.init_app(app)
    db.app = app
    db.create_all()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
