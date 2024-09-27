from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(email='aalejo@gmail.com').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("Admin privileges granted successfully!")
    else:
        print("User not found. Please check your email address.")
