from flask import Flask, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Category, Product
import csv

web_app = Flask(__name__)
web_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

def init_db():
    """ Initializes my database coming from models """
    db.init_app(web_app)
    db.app = web_app
    db.create_all()

    with open('categorias.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for collumn in reader:
            category = Category(name=collumn['nome'])
            db.session.add(category)
            db.session.commit()


@web_app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        products = Product.query.all()
        categories = Category.query.all()
        return render_template('index.html', products=products, categories=categories)





if __name__ == '__main__':
    init_db()
    web_app.run(debug=True)
