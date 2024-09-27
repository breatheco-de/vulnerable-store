from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from models import Product, User, db
from datetime import timedelta
import logging
from flask_session import Session
import redis

app = Flask(__name__)
app.config.from_object(Config)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Set session lifetime to 24 hours
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

Session(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

migrate = Migrate(app, db)
db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
    app.run(host='0.0.0.0', port=5000, debug=True)
