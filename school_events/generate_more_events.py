#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate additional Czech school events for testing
"""
from app import app, db, Event
from datetime import datetime, timedelta
import random

# Czech school events with descriptions
upcoming_events = [
    {
        "name": "Školní ples",
        "description": "Tradiční maturitní ples s hudbou, tancem a zábavou pro studenty a rodiče.",
        "days_ahead": 45
    },
    {
        "name": "Projektový den - Robotika",
        "description": "Workshop zaměřený na stavbu a programování robotů s Arduino.",
        "days_ahead": 15
    },
    {
        "name": "Lyžařský kurz",
        "description": "Týdenní lyžařský kurz v Krkonoších pro druhé ročníky.",
        "days_ahead": 60
    },
    {
        "name": "Anglický debatní klub",
        "description": "Setkání debatního klubu - téma: AI a budoucnost práce.",
        "days_ahead": 7
    },
    {
        "name": "Chemická olympiáda",
        "description": "Školní kolo chemické olympiády kategorie A a B.",
        "days_ahead": 20
    },
    {
        "name": "Filmový festival",
        "description": "Projekce studentských filmů a dokumentů v školní aule.",
        "days_ahead": 30
    },
    {
        "name": "Biologická exkurze",
        "description": "Návštěva botanické zahrady a přírodovědeckého muzea v Praze.",
        "days_ahead": 25
    },
    {
        "name": "Velikonoční trhy",
        "description": "Školní velikonoční jarmark s výrobky studentů.",
        "days_ahead": 120
    },
]

past_events = [
    {
        "name": "Seznamovací kurz",
        "description": "Týdenní pobyt pro nové studenty prvních ročníků.",
        "days_ago": 45
    },
    {
        "name": "Podzimní sběr",
        "description": "Sběr kaštanů a žaludů pro farmu a záchrannou stanici.",
        "days_ago": 30
    },
    {
        "name": "Halloween party",
        "description": "Školní Halloween párty s kostýmy a soutěžemi.",
        "days_ago": 15
    },
    {
        "name": "Přednáška - Kybernetická bezpečnost",
        "description": "Odborná přednáška o ochraně dat a bezpečnosti na internetu.",
        "days_ago": 10
    },
    {
        "name": "Fotografická soutěž",
        "description": "Vyhodnocení školní fotografické soutěže s tématikou přírody.",
        "days_ago": 20
    },
    {
        "name": "Divadelní představení",
        "description": "Návštěva divadelního představení Hamlet v Národním divadle.",
        "days_ago": 5
    },
]

def generate_events():
    with app.app_context():
        now = datetime.now()
        added_count = 0
        
        print("🎯 Generování nadcházejících akcí...")
        for event_data in upcoming_events:
            # Random time between 8:00 and 16:00
            hour = random.randint(8, 16)
            minute = random.choice([0, 15, 30, 45])
            
            event_date = now + timedelta(days=event_data["days_ahead"])
            event_date = event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            event = Event(
                name=event_data["name"],
                date=event_date,
                description=event_data["description"]
            )
            db.session.add(event)
            added_count += 1
            print(f"✓ Přidána akce: {event.name} ({event_date.strftime('%d.%m.%Y %H:%M')})")
        
        print("\n📚 Generování minulých akcí...")
        for event_data in past_events:
            # Random time between 8:00 and 16:00
            hour = random.randint(8, 16)
            minute = random.choice([0, 15, 30, 45])
            
            event_date = now - timedelta(days=event_data["days_ago"])
            event_date = event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            event = Event(
                name=event_data["name"],
                date=event_date,
                description=event_data["description"]
            )
            db.session.add(event)
            added_count += 1
            print(f"✓ Přidána akce: {event.name} ({event_date.strftime('%d.%m.%Y %H:%M')})")
        
        db.session.commit()
        print(f"\n🎉 Úspěšně přidáno {added_count} nových akcí!")
        print(f"📊 Nadcházející: {len(upcoming_events)}, Minulé: {len(past_events)}")

if __name__ == "__main__":
    generate_events()
