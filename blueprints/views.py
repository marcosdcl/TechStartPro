from flask import Blueprint, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from models import db, Category, Product

products_blueprint = Blueprint('views', __name__)

@products_blueprint.route('/', methods=['GET'])
def index():
    """ List all products from the database, if any """
    if request.method == 'GET':
        message = 0
        products = Product.query.all()
        categories = Category.query.all()
        if len(products) < 1:
            message = 1
        return render_template('index.html', products=products, categories=categories, message=message)


@products_blueprint.route('/', methods=['POST'])
def create():
    """ Create a new product in the database """
    if request.method == 'POST':
        try:
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
            
        except:
            return redirect('/')

    else:
        return redirect('/')


@products_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """ Update some product in the database """
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
        

@products_blueprint.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    """ Delete a product from the database """
    if request.method == 'GET':
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return redirect('/')

@products_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    """ Filter a product by a field or a combination of fields """
    if request.method == 'POST':
        message = 0
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

        return render_template('index.html', products=products, categories=categories, message=message)
        

    else:
        return redirect('/')
