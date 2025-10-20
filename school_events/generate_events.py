from app import app, db, Event
from datetime import datetime, timedelta
import random

events_data = [
    {
        'title': 'Programovací soutěž',
        'description': 'Soutěž v programování pro všechny ročníky. Tým 3-4 lidí.',
        'location': 'Učebna počítačů',
        'max_students': 40
    },
    {
        'title': 'Sportovní den',
        'description': 'Den plný sportovních aktivit - fotbal, volejbal, basketbal.',
        'location': 'Tělocvična',
        'max_students': 60
    },
    {
        'title': 'Vánoční besídka',
        'description': 'Tradiční vánoční setkání s programem a občerstvením.',
        'location': 'Aula',
        'max_students': 100
    },
    {
        'title': 'Exkurze do IT firmy',
        'description': 'Návštěva moderní IT firmy s prezentací a prohlídkou.',
        'location': 'Firma ABC, Praha',
        'max_students': 25
    },
    {
        'title': 'Hackathon 24h',
        'description': '24hodinový hackathon zaměřený na webové aplikace.',
        'location': 'Škola - celá',
        'max_students': 50
    },
    {
        'title': 'Den otevřených dveří',
        'description': 'Prezentace školy pro budoucí studenty a jejich rodiče.',
        'location': 'Celá škola',
        'max_students': 30
    },
    {
        'title': 'Přednáška o AI',
        'description': 'Přednáška odborníka z oblasti umělé inteligence.',
        'location': 'Aula',
        'max_students': 80
    },
    {
        'title': 'Turnaj v stolním tenise',
        'description': 'Školní turnaj v ping pongu, přihlášky na místě.',
        'location': 'Tělocvična',
        'max_students': 32
    },
    {
        'title': 'Workshop 3D tisku',
        'description': 'Praktický workshop o 3D modelování a tisku.',
        'location': 'Dílna',
        'max_students': 20
    },
    {
        'title': 'Filmový večer',
        'description': 'Promítání sci-fi filmů s následnou diskuzí.',
        'location': 'Aula',
        'max_students': 70
    },
]

with app.app_context():
    # Generate events for the next 3 months
    base_date = datetime.now()
    
    for i, event_data in enumerate(events_data):
        # Random date in the next 3 months
        days_ahead = random.randint(5, 90)
        event_date = base_date + timedelta(days=days_ahead)
        
        # Random time between 8:00 and 17:00
        hour = random.randint(8, 17)
        minute = random.choice([0, 15, 30, 45])
        event_time = datetime.strptime(f'{hour}:{minute}', '%H:%M').time()
        
        # Combine date and time
        event_datetime = datetime.combine(event_date.date(), event_time)
        
        event = Event(
            name=event_data['title'],
            description=event_data['description'],
            date=event_datetime
        )
        
        db.session.add(event)
        print(f'✓ Přidána akce: {event_data["title"]} ({event_datetime.strftime("%d.%m.%Y %H:%M")})')
    
    db.session.commit()
    print(f'\n🎉 Úspěšně přidáno {len(events_data)} nových akcí!')
