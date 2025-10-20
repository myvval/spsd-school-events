from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        db.session.delete(admin)
        db.session.commit()
        
    admin = User(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")