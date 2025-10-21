from app import app, db, Event, Registration, User
from datetime import datetime, timedelta
import random

def add_extra_event():
    with app.app_context():
        # Create new event
        new_event = Event(
            name="Graduation Ceremony",
            date=datetime(2026, 6, 30, 14, 0),  # June 30, 2026, 14:00
            description="End of year graduation ceremony celebrating our students' achievements. Family and friends welcome!"
        )
        
        db.session.add(new_event)
        db.session.commit()

        # Add random registrations for existing students
        students = User.query.filter_by(is_admin=False).all()
        
        for student in students:
            # 70% chance of registering
            if random.random() < 0.7:
                registration = Registration(
                    user_id=student.id,
                    event_id=new_event.id,
                    attended=False,
                    registration_date=datetime.now()
                )
                db.session.add(registration)
        
        db.session.commit()
        print("Added new event: Graduation Ceremony")

if __name__ == "__main__":
    add_extra_event()