from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_events.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    @staticmethod
    def validate_username(username):
        return len(username) >= 3
    
    @property
    def display_name(self):
        """Return name if available, otherwise username"""
        return self.name if self.name else self.username

def format_datetime(dt):
    """Format datetime with leading zeros removed from day and month"""
    day = str(dt.day)
    month = str(dt.month)
    return f"{day}.{month}.{dt.year} {dt.strftime('%H:%M')}"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')

    @property
    def formatted_date(self):
        return format_datetime(self.date)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    attended = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('registrations', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    events = Event.query.order_by(Event.date).all()
    return render_template('index.html', events=events)

@app.route('/students')
@login_required
def students():
    students = User.query.filter_by(is_admin=False).order_by(User.name, User.username).all()
    events = Event.query.order_by(Event.date).all()
    registrations = Registration.query.all()
    
    # Create a matrix of student registrations and attendance
    student_matrix = {}
    for student in students:
        student_matrix[student.id] = {}
        for event in events:
            registration = next((r for r in registrations if r.user_id == student.id and r.event_id == event.id), None)
            if registration:
                student_matrix[student.id][event.id] = {
                    'registered': True,
                    'attended': registration.attended,
                    'registration_id': registration.id
                }
            else:
                student_matrix[student.id][event.id] = {
                    'registered': False,
                    'attended': False,
                    'registration_id': None
                }
    
    return render_template('students.html', students=students, events=events, student_matrix=student_matrix)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')

        # Validate username length
        if not User.validate_username(username):
            flash('Username must be at least 3 characters long')
            return render_template('register.html')

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            name=name
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)

@app.route('/event/<int:event_id>/register')
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    if not Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first():
        registration = Registration(user_id=current_user.id, event_id=event_id)
        db.session.add(registration)
        db.session.commit()
        flash('Successfully registered for the event!')
    else:
        flash('You are already registered for this event!')
    return redirect(url_for('event_details', event_id=event_id))

@app.route('/admin/events')
@login_required
def admin_events():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    current_time = datetime.now()
    
    # Get current and future events
    current_events = Event.query.filter(Event.date >= current_time).order_by(Event.date).all()
    
    # Get past events
    previous_events = Event.query.filter(Event.date < current_time).order_by(Event.date.desc()).all()
    
    return render_template('admin_events.html', 
                         current_events=current_events,
                         previous_events=previous_events)

def validate_event_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        if date.year < 2025:
            return None, 'Event year cannot be earlier than 2025'
        return date, None
    except ValueError:
        return None, 'Invalid date format'

@app.route('/admin/events/create', methods=['POST'])
@login_required
def create_event():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    date_str = request.form.get('date')
    description = request.form.get('description')
    
    date, error = validate_event_date(date_str)
    if error:
        flash(error)
        return redirect(url_for('admin_events'))
    
    event = Event(name=name, date=date, description=description)
    db.session.add(event)
    db.session.commit()
    flash('Event created successfully!')
    return redirect(url_for('admin_events'))

@app.route('/admin/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.name = request.form.get('name')
        date_str = request.form.get('date')
        
        date, error = validate_event_date(date_str)
        if error:
            flash(error)
            return render_template('edit_event.html', event=event)
            
        event.date = date
        event.description = request.form.get('description')
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('admin_events'))
    
    return render_template('edit_event.html', event=event)

@app.route('/admin/registrations')
@login_required
def admin_registrations():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    query = request.args.get('query', '')
    event_id = request.args.get('event', '')
    
    # Get all events for the filter dropdown
    events = Event.query.order_by(Event.date.desc()).all()
    
    # Build the query
    registrations = Registration.query.join(User).join(Event)
    if query:
        registrations = registrations.filter(
            db.or_(User.name.contains(query), User.username.contains(query))
        )
    if event_id and event_id.isdigit():
        registrations = registrations.filter(Event.id == int(event_id))
    
    registrations = registrations.order_by(Event.date.desc()).all()
    return render_template('admin_registrations.html', 
                         registrations=registrations, 
                         query=query, 
                         events=events, 
                         selected_event=event_id)

@app.route('/admin/toggle_attendance/<int:registration_id>')
@login_required
def toggle_attendance(registration_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    registration = Registration.query.get_or_404(registration_id)
    registration.attended = not registration.attended
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return {'status': 'success', 'attended': registration.attended}
    return redirect(request.referrer or url_for('students'))

# API endpoints for React components
@app.route('/api/events')
def api_events():
    from datetime import datetime
    now = datetime.now()
    
    current_events = Event.query.filter(Event.date >= now.date()).order_by(Event.date).all()
    previous_events = Event.query.filter(Event.date < now.date()).order_by(Event.date.desc()).all()
    
    def event_to_dict(event):
        registered_count = Registration.query.filter_by(event_id=event.id).count()
        is_registered = False
        if current_user.is_authenticated and not current_user.is_admin:
            is_registered = Registration.query.filter_by(
                event_id=event.id, 
                user_id=current_user.id
            ).first() is not None
        
        return {
            'id': event.id,
            'title': event.name,
            'description': event.description,
            'date': event.date.isoformat(),
            'registered_count': registered_count,
            'is_registered': is_registered
        }
    
    return {
        'current': [event_to_dict(e) for e in current_events],
        'previous': [event_to_dict(e) for e in previous_events]
    }

@app.route('/api/students')
@login_required
def api_students():
    if not current_user.is_admin:
        return {'error': 'Unauthorized'}, 403
    
    students = User.query.filter_by(is_admin=False).all()
    
    students_data = []
    for student in students:
        event_count = Registration.query.filter_by(user_id=student.id).count()
        students_data.append({
            'id': student.id,
            'name': student.name or student.username,
            'username': student.username,
            'event_count': event_count
        })
    
    return students_data

@app.route('/admin/create_sample_data', methods=['POST'])
@login_required
def create_sample_data_route():
    if not current_user.is_admin:
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    try:
        from werkzeug.security import generate_password_hash
        import random
        from datetime import timedelta
        
        # Create sample events
        events = [
            Event(
                name="School Christmas Party",
                date=datetime(2025, 12, 20, 18, 0),
                description="Annual Christmas celebration with music, food, and fun activities."
            ),
            Event(
                name="Science Fair",
                date=datetime(2025, 11, 15, 13, 0),
                description="Students present their science projects. Prizes for best projects!"
            ),
            Event(
                name="Sports Day",
                date=datetime(2025, 10, 25, 9, 0),
                description="Annual sports competition with various athletic events and team games."
            )
        ]
        
        for event in events:
            db.session.add(event)
        db.session.commit()

        # Create sample students
        students = [
            "Anna Novotná", "Jan Svoboda", "Marie Dvořáková",
            "Petr Novák", "Tereza Černá", "Tomáš Procházka",
            "Lucie Kučerová", "Jakub Veselý", "Karolína Horáková", "David Král"
        ]

        for student_name in students:
            username = student_name.lower().replace(' ', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ý', 'y').replace('ř', 'r').replace('š', 's').replace('ž', 'z').replace('ů', 'u').replace('ú', 'u').replace('ó', 'o').replace('č', 'c')
            
            if not User.query.filter_by(username=username).first():
                student = User(
                    username=username,
                    password_hash=generate_password_hash('student123'),
                    name=student_name,
                    is_admin=False
                )
                db.session.add(student)
        db.session.commit()

        # Create random registrations
        students = User.query.filter_by(is_admin=False).all()
        events = Event.query.all()

        for student in students:
            for event in events:
                if random.random() < 0.7:
                    attended = random.random() < 0.8
                    registration = Registration(
                        user_id=student.id,
                        event_id=event.id,
                        attended=attended,
                        registration_date=datetime.now() - timedelta(days=random.randint(1, 30))
                    )
                    db.session.add(registration)
        
        db.session.commit()
        flash('Sample data created successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating sample data: {str(e)}')
    
    return redirect(url_for('index'))

@app.route('/admin/create_previous_data', methods=['POST'])
@login_required
def create_previous_data_route():
    if not current_user.is_admin:
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    try:
        from werkzeug.security import generate_password_hash
        import random
        from datetime import timedelta
        
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

        students = User.query.filter_by(is_admin=False).all()
        if not students:
            student_names = [
                "Eva Malá", "Martin Horák", "Zuzana Šimková",
                "Filip Kovář", "Nina Benešová", "Ondřej Marek",
                "Klára Říhová", "Adam Tichý", "Barbora Vávrová",
                "Daniel Pospíšil", "Sofie Marková", "Matěj Kříž"
            ]
            
            for name in student_names:
                username = name.lower().replace(' ', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ý', 'y').replace('ř', 'r').replace('š', 's').replace('ž', 'z').replace('ů', 'u').replace('ú', 'u').replace('ó', 'o').replace('č', 'c')
                student = User(
                    username=username,
                    password_hash=generate_password_hash('student123'),
                    name=name,
                    is_admin=False
                )
                db.session.add(student)
                students.append(student)
            db.session.commit()

        for event in db_events:
            if "Concert" in event.name or "Exhibition" in event.name:
                num_registrations = random.randint(15, 20)
            elif "Olympics" in event.name or "Tournament" in event.name:
                num_registrations = random.randint(8, 12)
            else:
                num_registrations = random.randint(10, 15)

            event_students = random.sample(students, min(num_registrations, len(students)))

            for student in event_students:
                attended = random.random() < (0.85 if "Olympics" not in event.name else 0.75)
                
                registration = Registration(
                    user_id=student.id,
                    event_id=event.id,
                    attended=attended,
                    registration_date=event.date - timedelta(days=random.randint(5, 20))
                )
                db.session.add(registration)
        
        db.session.commit()
        flash('Previous sample data created successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating previous data: {str(e)}')
    
    return redirect(url_for('index'))

@app.route('/admin/generate_events', methods=['POST'])
@login_required
def generate_events_route():
    if not current_user.is_admin:
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    try:
        import random
        from datetime import timedelta
        
        # Generate new future event
        event_types = [
            ("Graduation Ceremony", "End of year graduation ceremony celebrating our students' achievements. Family and friends welcome!"),
            ("Technology Workshop", "Hands-on workshop exploring latest technology trends and innovations."),
            ("Drama Performance", "Student theatrical production showcasing dramatic talents."),
            ("Field Trip", "Educational excursion to local museum and historical sites."),
            ("Dance Competition", "Annual dance showcase with various styles and performances."),
            ("Debate Tournament", "Inter-class debate competition on current events and social issues."),
            ("Music Festival", "Multi-genre music festival featuring student bands and solo performers."),
            ("Cooking Class", "Interactive culinary workshop learning international cuisines."),
            ("Photography Exhibition", "Display of student photography from various themes and techniques."),
            ("Environmental Day", "Activities focused on sustainability and environmental awareness.")
        ]
        
        # Pick a random event type
        event_name, event_desc = random.choice(event_types)
        
        # Generate a future date (1-6 months from now)
        days_ahead = random.randint(30, 180)
        event_date = datetime.now() + timedelta(days=days_ahead)
        event_date = event_date.replace(hour=random.choice([9, 10, 13, 14, 15, 17, 18]), minute=random.choice([0, 30]))
        
        new_event = Event(
            name=event_name,
            date=event_date,
            description=event_desc
        )
        
        db.session.add(new_event)
        db.session.commit()

        # Add random registrations for existing students
        students = User.query.filter_by(is_admin=False).all()
        
        for student in students:
            if random.random() < 0.6:  # 60% chance of registering
                registration = Registration(
                    user_id=student.id,
                    event_id=new_event.id,
                    attended=False,
                    registration_date=datetime.now()
                )
                db.session.add(registration)
        
        db.session.commit()
        flash(f'Generated new event: {event_name}')
    except Exception as e:
        db.session.rollback()
        flash(f'Error generating event: {str(e)}')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)