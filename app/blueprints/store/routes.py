from .import bp as store
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Product, Cart, User

# ROUTES


#show all available products
@store.route('/', methods = ['GET', 'POST'])
def index():
    products=Product.query.all()
    return render_template('index.html.j2', products=products)
  
#return single product 3:
@store.route('/product/<int:id>')
def get_a_product(id):
    product = Product.query.get(id)
    return render_template('single_product.html.j2', product=product, view_all=True)


@store.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart=Cart.query.all()
    return render_template("cart.html.j2", cart=cart )
#add to cart
@store.route('/cart/<int:id>')
@login_required
def add_to_cart(id):
    product=Product.query.get(id)
    current_user.cart_items(product)
    flash(f"Congrats {product} was added to your cart")
    return redirect(url_for("store.index"))
    # if product:
    #     current_user.products.append(product)
    #     flash(f"{product.name} has been added to your cart", "success")
    # else:
    #     flash("That item does not exist")
    # return redirect(url_for('store.index'))




@store.route('/delete_item/<int:id>')
@login_required
def delete_item(id):
    product = Product.query.get(id)
    current_user.remove_item(product)
    # cart = Cart.query.get(id)
    # if cart and cart.cart_id != current_user.id:
    #     flash('error', 'danger')
    #     return redirect(url_for('store.index'))
    # cart.delete()
    flash('You successfully removed item', 'info')
    return redirect(request.referrer or url_for('store.index'))


