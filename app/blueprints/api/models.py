from app import db, login
from flask_login import UserMixin # IS ONLY FOR THE USER MODEL!!!!
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    email =  db.Column(db.String, unique=True, index=True)
    password =  db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    products = db.relationship("Products", 
                    secondary = "cart",
                    backref="shopper", 
                    lazy='dynamic')

    
    
    def __repr__(self):
        return f'<User: {self.id}|{self.first_name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def edit(self, new_desc):
        self.body=new_desc
    
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.first_name
        }
    
    def is_shopping(self, products):
        if not self.user(products):
            self.user.append(products)
            db.session.commit()

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('product.id'))
    id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    desc = db.Column(db.Text)
    price = db.Column(db.Float)
    img=db.Column(db.String)

    def __repr__(self):
        return f'<Item: {self.id}|{self.name}>'

    def edit(self, new_desc):
        self.body=new_desc

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'desc':self.desc,
            'price':self.price,
            'img':self.img,
            'created_on':self.created_on,
            'category_id':self.category_id
        }

    def from_dict(self, data):
        for field in ['name','desc','price','img','category_id']:
            if field in data:
                    #the object, the attribute, value
                setattr(self, field, data[field])