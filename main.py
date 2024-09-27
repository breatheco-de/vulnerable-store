from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from models import Product, User, db

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def add_sample_products():
    sample_products = [
        Product(name='Laptop',
                description='A high-performance laptop',
                price=999.99,
                stock=10),
        Product(name='Smartphone',
                description='Latest smartphone model',
                price=599.99,
                stock=20),
        Product(name='Headphones',
                description='Noise-cancelling headphones',
                price=199.99,
                stock=30)
    ]
    for product in sample_products:
        db.session.add(product)
    db.session.commit()


from routes import auth, shop, admin

app.register_blueprint(auth.bp)
app.register_blueprint(shop.bp)
app.register_blueprint(admin.bp)


@app.route('/')
def index():
    return shop.index()


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     if Product.query.count() == 0:
    #         add_sample_products()
    app.run(host='0.0.0.0', port=8000, debug=True)
