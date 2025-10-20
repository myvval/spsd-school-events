import os
from sqlalchemy import MetaData
from app import app, db, User, Event, Registration

# Delete the database file if it exists
db_path = os.path.join(os.path.dirname(__file__), 'school_events.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print("Deleted existing database.")

# Drop all tables and recreate them
with app.app_context():
    meta = MetaData()
    meta.reflect(bind=db.engine)
    meta.drop_all(bind=db.engine)
    db.create_all()
    print("Created new database with updated schema.")