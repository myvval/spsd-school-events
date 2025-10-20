from app import app, db, User, Event, Registration
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        # Create sample events
        events = [
            Event(
                name="School Christmas Party",
                date=datetime(2025, 12, 20, 18, 0),  # December 20, 2025, 18:00
                description="Annual Christmas celebration with music, food, and fun activities."
            ),
            Event(
                name="Science Fair",
                date=datetime(2025, 11, 15, 13, 0),  # November 15, 2025, 13:00
                description="Students present their science projects. Prizes for best projects!"
            ),
            Event(
                name="Sports Day",
                date=datetime(2025, 10, 25, 9, 0),   # October 25, 2025, 9:00
                description="Annual sports competition with various athletic events and team games."
            )
        ]
        
        # Add events to database
        for event in events:
            db.session.add(event)
        db.session.commit()

        # Create sample students
        students = [
            "Anna Novotná",
            "Jan Svoboda",
            "Marie Dvořáková",
            "Petr Novák",
            "Tereza Černá",
            "Tomáš Procházka",
            "Lucie Kučerová",
            "Jakub Veselý",
            "Karolína Horáková",
            "David Král"
        ]

        # Add students to database
        for student_name in students:
            # Create username from name
            username = student_name.lower().replace(' ', '')
            
            # Check if student already exists
            if not User.query.filter_by(username=username).first():
                student = User(
                    username=username,
                    password_hash=generate_password_hash('student123'),  # Default password for all students
                    name=student_name,  # Add the student's full name
                    is_admin=False
                )
                db.session.add(student)
        db.session.commit()

        # Create random registrations and attendance
        students = User.query.filter_by(is_admin=False).all()
        events = Event.query.all()

        for student in students:
            for event in events:
                # 70% chance of registering for each event
                if random.random() < 0.7:
                    # If registered, 80% chance of attending
                    attended = random.random() < 0.8
                    registration = Registration(
                        user_id=student.id,
                        event_id=event.id,
                        attended=attended,
                        registration_date=datetime.now() - timedelta(days=random.randint(1, 30))
                    )
                    db.session.add(registration)
        
        db.session.commit()
        print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()