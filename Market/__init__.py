from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
# URI - Unified Resource Identifier
app.config['SECRET_KEY']='80854d81e0d43c51e0aa3225'
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy(app=app)
bcrypt=Bcrypt(app=app)
login_manager=LoginManager(app=app)
from Market import routes 

with app.app_context():
    db.create_all()
    from Market.models import Item
    
    # Check if Item table is empty
    if Item.query.count() == 0:
        default_items = [
            Item(name='Laptop', price=50000, barcode='123456789012', description='High performance laptop'),
            Item(name='Phone', price=30000, barcode='123456789013', description='Latest smartphone'),
            Item(name='Keyboard', price=2000, barcode='123456789014', description='Mechanical keyboard'),
            Item(name='Mouse', price=1000, barcode='123456789015', description='Wireless mouse'),
            Item(name='Monitor', price=15000, barcode='123456789016', description='24 inch LED monitor')
        ]
        db.session.add_all(default_items)
        db.session.commit()
        print("Default items added to database")  