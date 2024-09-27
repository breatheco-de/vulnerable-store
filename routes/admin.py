from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Product, Order, db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('shop.index'))

@bp.route('/')
def dashboard():
    orders = Order.query.order_by(Order.id.desc()).limit(10).all()
    return render_template('admin/dashboard.html', orders=orders)

@bp.route('/products')
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        
        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/add_product.html')

@bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/edit_product.html', product=product)

@bp.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('admin.products'))
