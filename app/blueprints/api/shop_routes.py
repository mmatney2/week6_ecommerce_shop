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



@api.get('/product')
# @token_auth.login_required()
def get_product():
    products = Product.query.all()   
    products_dicts = [product.to_dict() for product in products]
    return make_response({"products":products_dicts},200)

@api.get('/product/<int:id>')
# @token_auth.login_required()
def get_single_product_info(id):
    product = Product.query.all(id)   

    if not product:
        abort(404)
    product_dict = product.to_dict()
    return make_response(f"Product {product_dict} with ID {product.id} has the following details. ", 200)


#customer add item to their cart if they're logged in:
@api.post('/cart/<int:id>')
@token_auth.login_required()
def add_item_to_cart(id):
    products = Product.query.get(id)
    if not products:
        abort(404)
    cart=Cart
    cart.save()
    add_items_to_cart = [item.to_dict() for item in products.products]
    g.current_user.products.append(cart)
    g.current_user.save()
    return make_response({"Product": add_items_to_cart},200)

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



