"""
Script to add name field to existing users in the database.
This will add a 'name' column to the User table if it doesn't exist.
"""
from app import app, db, User

def add_name_field():
    with app.app_context():
        # Check if name column exists by trying to access it
        try:
            # Try to query with name field
            User.query.with_entities(User.name).first()
            print("Name field already exists!")
        except:
            print("Adding name field to database...")
            # Add the name column
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE user ADD COLUMN name VARCHAR(100)"))
                conn.commit()
            print("Name field added successfully!")
        
        # Optionally, copy username to name for existing users who don't have a name
        users_without_name = User.query.filter(db.or_(User.name == None, User.name == '')).all()
        if users_without_name:
            print(f"\nFound {len(users_without_name)} users without names.")
            print("Setting their name to their username as default...")
            for user in users_without_name:
                user.name = user.username
            db.session.commit()
            print("Default names set successfully!")
        else:
            print("\nAll users have names set.")

if __name__ == '__main__':
    add_name_field()
