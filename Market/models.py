from Market import db,bcrypt
from flask_login import UserMixin

class Item(db.Model):   
    # __table__='shop_items'
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    barcode=db.Column(db.String(length=12),nullable=False,unique=True)
    description=db.Column(db.String(length=10240),nullable=False,unique=True)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def buy(self,user):
        self.owner=user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self,user):
        self.owner=None
        user.budget +=self.price
        db.session.commit()


class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    UserName=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(),nullable=False,unique=True)
    password_hash=db.Column(db.String(),nullable=False)
    budget=db.Column(db.Integer(),default=100000, nullable=False)
    items=db.relationship('Item',backref='owned_user',lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{str(self.budget)}$'


    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('Utf-8')
    

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
        #returns True if the we pass the corrcetion password of this particular user object
    
    def can_purchase(self,item_obj):
        return self.budget >=item_obj.price
    
    def can_sell(self,item_obj):
        return item_obj in self.items
    
    