from Market import db,bcrypt

class Item(db.Model):   
    # __table__='shop_items'
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    barcode=db.Column(db.String(length=12),nullable=False,unique=True)
    description=db.Column(db.String(length=10240),nullable=False,unique=True)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))


class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    UserName=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(),nullable=False,unique=True)
    password_hash=db.Column(db.String(),nullable=False)
    budget=db.Column(db.Integer(),default=1000, nullable=False)
    items=db.relationship('Item',backref='owned_user',lazy=True)


    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('Utf-8')
