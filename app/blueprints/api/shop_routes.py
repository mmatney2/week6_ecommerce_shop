from . import bp as api
from app.blueprints.auth.auth import token_auth
from flask import request, make_response, g, abort
from .models import *
from ...helpers import require_admin


# ############
# ##
# ##  CATEGORY API ROUTES
# ##
# ############


# Get all the Categories

@api.get('/product')
# @token_auth.login_required()
def get_product():
    products = Product.query.all()   
    products_dicts = [products.to_dict() for product in products]
    return make_response({"products":products_dicts},200)

@api.get('/product/<string:name>')
# @token_auth.login_required()
def get_single_product_info(name):
    product_dict = request.get_json()

    ps = Product.query.get(name)
    for p in ps:
        if not p:
            abort(404)
        p = Product()
        p.from_dict(product_dict)
        p.save()
        return make_response(f"Product {p.name} with ID {p.id} has the following details. ", 200)

#show items in the cart:        
# @api.post('/cart')
# @token_auth.login_required()
# def add_item_to_cart(id):
#     cart_dict = request.get_json()
#     if not all(key in cart_dict for key in ('name', 'desc', 'price', 'img','category_id')):
#         abort(400)
#     product=Product()
#     product.from_dict(cart_dict)
#     product.save()
#     return make_response(f"Product {product.name} was added with an id {product.id}",200)

#customer add item to their cart if they're logged in:
@api.post('/cart/<int:id>')
@token_auth.login_required()
def add_item_to_cart(id):
    cart_item = request.get_json()
    cart = Cart(**cart_item)
    cart.save()
    g.current_user.products.append(cart)
    g.current_user.save()
    return make_response(f"Product {cart.name} was added with an id {cart.id}",200)

#show cart
# @api.post('/cart')
# @token_auth.login_required()
# def cart():
#     cart_dict = request.get_json()
#     if not all(key in cart_dict for key in ('name', 'desc', 'price', 'img','category_id')):
#         abort(400)
#     cart=Cart()
#     cart = cart.from_dict(cart_dict)
#     return make_response(f"Here are the items in your cart: {cart}",200)
    
#show cart
@api.get('/cart')
@token_auth.login_required()
def cart():
    products = g.current_user.add_item_to_cart()
    products = [product.to_dict() for product in products]
    cart_dict = Cart.query.all()   
    if not all(key in cart_dict for key in ('name', 'desc', 'price', 'img','category_id')):
        abort(400)
    cart=Cart()
    cart = cart.from_dict(cart_dict)
    return make_response(f"Here are the items in your cart: {cart}",200)

# Delete whole cart
@api.delete('/item/<int:id>')
@token_auth.login_required()
@require_admin
def delete_cart(id):
    product_to_delete = Product.query.get(id)
    if not product_to_delete:
        abort(404)
    product_to_delete.delete()
    return make_response(f"Item with id: {id} has been deleted", 200)

# Delete a Item by ID
@api.delete('/item/<int:id>')
@token_auth.login_required()
@require_admin
def delete_item(id):
    product_to_delete = Product.query.get(id)
    for p in product_to_delete:
        if not p:
            abort(404)
        p.delete()
    return make_response(f"Item with id: {id} has been deleted", 200)



