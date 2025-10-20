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

@app.route('/admin/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!')
    return redirect(url_for('admin_events'))

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
    
    current_events = Event.query.filter(Event.date >= now.date()).order_by(Event.date, Event.time).all()
    previous_events = Event.query.filter(Event.date < now.date()).order_by(Event.date.desc(), Event.time.desc()).all()
    
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
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'time': event.time.strftime('%H:%M'),
            'location': event.location,
            'max_students': event.max_students,
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)