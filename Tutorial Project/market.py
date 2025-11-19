from flask import Flask ,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
# URI - Unified Resource Identifier
db=SQLAlchemy(app=app)

class Item(db.Model):

    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    barcode=db.Column(db.String(length=12),nullable=False,unique=True)
    description=db.Column(db.String(length=10240),nullable=False,unique=True)

print("hello")
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')
@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the about page of {username}'
@app.route('/market')
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('market.html',items=items)
if __name__=='__main__':
    # from market import app, db
    with app.app_context():
        db.create_all()
    app.run(debug=True)
