from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from models import db, Category, Product
import csv

web_app = Flask(__name__)
web_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

def init_db():
    """ Initializes my database coming from models """
    db.init_app(web_app)
    db.app = web_app
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


@web_app.route('/', methods=['GET'])
def index():

    if request.method == 'GET':
        products = Product.query.all()
        categories = Category.query.all()
        return render_template('index.html', products=products, categories=categories)


@web_app.route('/', methods=['POST'])
def create():

    if request.method == 'POST':
        new_product = Product(
            name = request.form['name'], 
            description = request.form['description'], 
            value = request.form['value']
        )
        db.session.add(new_product)
        db.session.commit()

        categories = request.form.getlist('category')
        for category in categories:
            cat = Category.query.filter_by(id=category).first()
            cat.products.append(new_product)
            db.session.commit()

        return redirect('/')

    else:
        return render_template('index.html')


@web_app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    product = Product.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == 'POST':
        product.name = request.form['name'] 
        product.description = request.form['description']
        product.value = request.form['value']
        product.category = ([])
        db.session.commit()

        categories = request.form.getlist('category')
        for category in categories:
            cat = Category.query.filter_by(id=category).first()
            cat.products.append(product)
            db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', product=product, categories=categories)
        

@web_app.route('/delete/<int:id>', methods=['GET'])
def delete(id):

    if request.method == 'GET':
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return redirect('/')

@web_app.route('/search', methods=['GET', 'POST'])
def filter():

    if request.method == 'POST':

        products = Product.query.all()
        categories = Category.query.all()

        filters = []
        columns = ['name','description','value']
        search_by_category = request.form['category']
        search_by_text = request.form['filter_text']

        if search_by_category == 'all':
            for col in columns:
                filters.append(getattr(Product, col).like("%%%s%%" % search_by_text))
            products = Product.query.filter(or_(*filters))
        else:
            for col in columns:
                filters.append(getattr(Product, col).like("%%%s%%" % search_by_text))
            products = db.session.query(Product).filter(or_(*filters)).join(Product.category).filter(Category.name.like(search_by_category))

        return render_template('filtered.html', products=products, categories=categories)
        

    else:
        return redirect('/')

if __name__ == '__main__':
    init_db()
    web_app.run(debug=True)
