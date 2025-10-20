from app import app, db, User, Event, Registration
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_previous_events():
    with app.app_context():
        # Sample past events with varied dates and types
        past_events = [
            {
                "name": "Spring Concert 2025",
                "date": datetime(2025, 5, 15, 17, 30),
                "description": "Annual spring concert featuring student performances in choir and instrumental music."
            },
            {
                "name": "Math Olympics",
                "date": datetime(2025, 4, 20, 9, 0),
                "description": "Mathematics competition with challenging problems and puzzles."
            },
            {
                "name": "Career Day",
                "date": datetime(2025, 3, 12, 10, 0),
                "description": "Professional speakers sharing career insights and opportunities."
            },
            {
                "name": "Art Exhibition",
                "date": datetime(2025, 2, 28, 14, 0),
                "description": "Showcase of student artwork from various mediums and styles."
            },
            {
                "name": "Winter Sports Tournament",
                "date": datetime(2025, 1, 25, 8, 30),
                "description": "Indoor sports competition including basketball and volleyball."
            },
            {
                "name": "Literature Festival",
                "date": datetime(2024, 12, 10, 13, 0),
                "description": "Celebration of reading and writing with author visits and workshops."
            }
        ]

        # Add events to database
        db_events = []
        for event_data in past_events:
            event = Event(
                name=event_data["name"],
                date=event_data["date"],
                description=event_data["description"]
            )
            db.session.add(event)
            db_events.append(event)
        db.session.commit()

        # Get existing students or create new ones if needed
        students = User.query.filter_by(is_admin=False).all()
        if not students:
            # Create sample students if none exist
            student_names = [
                "Eva Malá", "Martin Horák", "Zuzana Šimková",
                "Filip Kovář", "Nina Benešová", "Ondřej Marek",
                "Klára Říhová", "Adam Tichý", "Barbora Vávrová",
                "Daniel Pospíšil", "Sofie Marková", "Matěj Kříž"
            ]
            
            for name in student_names:
                username = name.lower().replace(' ', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ý', 'y').replace('ř', 'r').replace('š', 's').replace('ž', 'z').replace('ů', 'u').replace('ú', 'u')
                student = User(
                    username=username,
                    password_hash=generate_password_hash('student123'),
                    name=name,
                    is_admin=False
                )
                db.session.add(student)
                students.append(student)
            db.session.commit()

        # Create registrations with realistic attendance patterns
        for event in db_events:
            # Determine number of registrations based on event type
            if "Concert" in event.name or "Exhibition" in event.name:
                num_registrations = random.randint(15, 20)  # Popular events
            elif "Olympics" in event.name or "Tournament" in event.name:
                num_registrations = random.randint(8, 12)   # Competitive events
            else:
                num_registrations = random.randint(10, 15)  # Regular events

            # Select random students for this event
            event_students = random.sample(students, min(num_registrations, len(students)))

            # Create registrations with varied attendance
            for student in event_students:
                # More likely to attend regular events, slightly less for competitions
                attended = random.random() < (0.85 if "Olympics" not in event.name else 0.75)
                
                registration = Registration(
                    user_id=student.id,
                    event_id=event.id,
                    attended=attended,
                    registration_date=event.date - timedelta(days=random.randint(5, 20))
                )
                db.session.add(registration)
        
        db.session.commit()
        print("Previous events and registrations created successfully!")

if __name__ == "__main__":
    create_previous_events()