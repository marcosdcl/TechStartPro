from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Creates the relationship table
product_category = db.Table('product_category',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Category(db.Model):
    """ Create the category table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

class Product(db.Model):
    """ Create the product table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    value = db.Column(db.Float, nullable=False)
    category = db.relationship('Category', secondary = product_category,
        backref = db.backref('products', lazy = 'dynamic')
    )

    def __repr__(self):
        return '<Product %r>' % self.name
