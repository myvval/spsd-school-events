from app import app, db, User
from werkzeug.security import generate_password_hash
try:
    from config import ADMIN_USERNAME, ADMIN_PASSWORD
except ImportError:
    print("Error: config.py not found!")
    print("Please create config.py with ADMIN_USERNAME and ADMIN_PASSWORD")
    exit(1)

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(username=ADMIN_USERNAME).first()
    if admin:
        db.session.delete(admin)
        db.session.commit()
        
    admin = User(
        username=ADMIN_USERNAME,
        password_hash=generate_password_hash(ADMIN_PASSWORD),
        name='Administrator',
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user '{ADMIN_USERNAME}' created successfully!")
    print("Credentials are stored in config.py (not in Git)")