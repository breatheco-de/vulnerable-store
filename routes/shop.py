from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from models import Product, Order, OrderItem, db

bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@bp.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    products = Product.query.filter(Product.id.in_(cart_items.keys())).all()
    return render_template('cart.html', cart_items=cart_items, products=products)

@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    cart[product_id] = cart.get(product_id, 0) + quantity
    session.modified = True
    
    return jsonify({'success': True, 'cart_count': sum(cart.values())})

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        cart_items = session.get('cart', {})
        if not cart_items:
            return redirect(url_for('shop.cart'))
        
        total = 0
        order = Order(user_id=current_user.id, status='pending', total=0)
        db.session.add(order)
        
        for product_id, quantity in cart_items.items():
            product = Product.query.get(product_id)
            if product and product.stock >= quantity:
                total += product.price * quantity
                order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=product.price)
                db.session.add(order_item)
                product.stock -= quantity
            else:
                db.session.rollback()
                flash(f'Not enough stock for {product.name}')
                return redirect(url_for('shop.cart'))
        
        order.total = total
        db.session.commit()
        session.pop('cart', None)
        flash('Your order has been placed successfully!')
        return redirect(url_for('shop.index'))
    
    return render_template('checkout.html')


# New vulnerable code

    @bp.route('/order/<int:order_id>')
    @login_required
    def order_detail(order_id):
        order = Order.query.get(order_id)
        return render_template('order_detail.html', order=order)
    

# New vulnerable code

    @bp.route('/order/<int:order_id>')
    @login_required
    def order_detail(order_id):
        order = Order.query.get(order_id)
        return render_template('order_detail.html', order=order)
    

# New vulnerable code

    @bp.route('/order/<int:order_id>')
    @login_required
    def order_detail(order_id):
        order = Order.query.get(order_id)
        return render_template('order_detail.html', order=order)
    

# New vulnerable code

    @bp.route('/order/<int:order_id>')
    @login_required
    def order_detail(order_id):
        order = Order.query.get(order_id)
        return render_template('order_detail.html', order=order)
    