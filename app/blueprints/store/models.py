from app import db
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from app import db, login
from flask_login import UserMixin # IS ONLY FOR THE USER MODEL!!!!
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    email =  db.Column(db.String, unique=True, index=True)
    password =  db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    products = db.relationship('Product', 
                    secondary="cart", 
                    backref='shopper', 
                    lazy="dynamic")
   

   

# should return a unique identifing string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    # Human readbale ver of rpr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])

    # save the user to the database
    def save(self):
        db.session.add(self) #adds the user to the db session
        db.session.commit() #save everythig in the session to the db

    def cart_items(self, cart_item):
        self.products.append(cart_item)
        db.session.commit()
    def remove_item(self, cart_item):
        self.products.remove(cart_item)
        db.session.commit()

    def to_dict(self):
        return {
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'created_on':self.created_on,
        }
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???

class Cart(UserMixin, db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Product(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    desc = db.Column(db.Text)
    price = db.Column(db.Float)
    img=db.Column(db.String)
    created_on=db.Column(db.DateTime, index=True, default=dt.utcnow)

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
        }

    def from_dict(self, data):
        for field in ['name','desc','price','img','created_on']:
            if field in data:
                    #the object, the attribute, value
                setattr(self, field, data[field])

    def cart_items(self, cart_item):
        self.products.append(cart_item)
        db.session.commit()

    def remove_item(self, cart_item):
        self.products.remove(cart_item)
        db.session.commit()
