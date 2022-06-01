from .import bp as store
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Product, Cart, User

# ROUTES
#register a user:

@store.post("/user")
def post_item():
    user_dict=request.get_json()
    users = User()
    users.from_dict(user_dict)
    users.save()
    return render_template()    

# Create new Cat
# {
#     "name":"my cat name"
# }
@store.post('/product')
def post_category():
    prod_name = request.get_json().get("name")
    product = Product(name = prod_name)
    product.save()
    return make_response(f"category {product.id} with name {product.name} created", 200)    

# Get all Products 2
@store.get('/product')
def get_product():
    products=Product.query.all()
    product_dicts=[product.to_dict() for product in products]
    return make_response({"products":product_dicts},200)

  
#return single product 3:

@store.get('/product/<int:id>')
def get_post(id):
    product = Product.query.get(id)
    if not product:
        abort(404)
    product_dict= product.to_dict() 
    return make_response(product_dict, 200)       

#customer add item to their cart if they're logged in 4:
@store.post('/cart/<int:id>')
def add_item_to_cart(id):
    products = Product.query.get(id)
    if not products:
        abort(404)
    cart=Cart()
    cart.save()
    add_items_to_cart = [item.to_dict() for item in products.products]
    g.current_user.products.append(cart)
    g.current_user.save()
    return make_response({"Product": add_items_to_cart},200)

#show cart 5
@store.get('/cart')
def cart():
    products = g.current_user.add_item_to_cart()
    products = [product.to_dict() for product in products]
    cart_dict = Cart.query.all()   
    if not all(key in cart_dict for key in ('name', 'desc', 'price', 'img','category_id')):
        abort(400)
    cart=Cart()
    cart = cart.from_dict(cart_dict)
    return make_response(f"Here are the items in your cart: {cart}",200)


# Delete whole cart 6
@store.delete('/item/<int:id>')
def delete_cart(id):
    product_to_delete = Product.query.get(id)
    if not product_to_delete:
        abort(404)
    product_to_delete.delete()
    return make_response(f"Item with id: {id} has been deleted", 200)

# Delete a Item by ID 7
@store.delete('/item/<int:id>')
def delete_item(id):
    product_to_delete = Product.query.get(id)
    for p in product_to_delete:
        if not p:
            abort(404)
        p.delete()
    return make_response(f"Item with id: {id} has been deleted", 200)

