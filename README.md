# 📅 SPŠD Školní akce - School Events Management System

A modern web application for managing school events, student registrations, and attendance tracking. Built with Flask and React.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![React](https://img.shields.io/badge/react-18.2.0-61dafb.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 🎯 For Students
- **Browse Events**: View all upcoming and past school events with search and filtering
- **Easy Registration**: One-click registration for events
- **Personal Dashboard**: Track your registered events and attendance history
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### 👨‍🏫 For Administrators
- **Event Management**: Create, edit, and delete events with detailed information
- **Attendance Tracking**: Mark student attendance with toggle switches
- **Registration Overview**: View all student registrations per event
- **Student Management**: View all students with their event participation statistics
- **Categorized Interface**: Organized dashboard with clear sections for different tasks

### 🎨 Design Features
- **Modern UI**: Clean, professional interface with blue gradient theme
- **Dark Mode**: Full dark theme support that persists across sessions
- **Responsive Tables**: Mobile-friendly data presentation
- **Real-time Search**: Instant filtering for events and students
- **Czech Localization**: Complete Czech language support

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/myvval/spsd-school-events.git
   cd spsd-school-events/school_events
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-login flask-sqlalchemy werkzeug
   ```

4. **Initialize the database**
   ```bash
   python rebuild_db.py
   ```

5. **Create an admin account**
   ```bash
   python create_admin.py
   ```
   Follow the prompts to set admin username and password.

6. **Generate sample data** (optional)
   ```bash
   python generate_events.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Open in browser**
   Navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
school_events/
├── app.py                          # Main Flask application
├── static/
│   ├── style.css                   # Main stylesheet with theme system
│   ├── react-styles.css            # React component styles
│   ├── js/
│   │   ├── events-react.js         # Events list React component
│   │   └── students-react.js       # Students list React component
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── index.html                  # Events page
│   ├── students.html               # Students page
│   ├── admin_events.html           # Admin event management
│   ├── admin_registrations.html    # Registration management
│   ├── edit_event.html             # Event editor
│   ├── event_details.html          # Event details view
│   ├── login.html                  # Login page
│   └── register.html               # User registration
├── instance/
│   └── school_events.db            # SQLite database
├── create_admin.py                 # Admin account creator
├── generate_events.py              # Sample data generator
└── rebuild_db.py                   # Database initializer
```

## 🔐 Default Credentials

After running `create_admin.py`, use your chosen credentials.

**Sample Users** (if you ran `create_sample_data.py`):
- Username: `student1` / Password: `password`
- Username: `student2` / Password: `password`

## 🎨 Theme System

The application features a comprehensive theme system with two modes:

### Light Mode
- Clean white backgrounds
- Blue accent colors (#2563eb, #3b82f6)
- High contrast for readability

### Dark Mode
- Dark navy backgrounds (#0c1829, #1e293b)
- Blue highlights for better night viewing
- Reduced eye strain

**Toggle theme**: Click the 🌙/☀️ button in the navigation bar.

## 📊 Database Schema

### Models

**User**
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `name`: Display name
- `is_admin`: Admin flag

**Event**
- `id`: Primary key
- `name`: Event name
- `date`: Event date and time
- `description`: Event details
- `registrations`: Relationship to registrations

**Registration**
- `user_id`: Foreign key to User
- `event_id`: Foreign key to Event
- `attended`: Attendance status

## 🛠️ Development

### API Endpoints

**Public Endpoints**
- `GET /api/events` - Get all events (current and past)
- `POST /register/<event_id>` - Register for event (requires login)
- `POST /unregister/<event_id>` - Unregister from event (requires login)

**Admin Endpoints** (requires admin privileges)
- `GET /api/students` - Get all students with statistics
- `POST /admin/events/create` - Create new event
- `POST /admin/events/<event_id>/edit` - Update event
- `POST /admin/events/<event_id>/delete` - Delete event
- `POST /admin/toggle-attendance` - Toggle student attendance

### Adding New Features

1. **Backend**: Add routes in `app.py`
2. **Frontend**: Create React components in `static/js/`
3. **Styles**: Update `style.css` or `react-styles.css`
4. **Database**: Modify models in `app.py` and run `rebuild_db.py`

## 🎯 Usage Guide

### For Students

1. **Register an Account**
   - Click "Registrace" in the navigation
   - Enter username, name, and password
   - Login with your credentials

2. **Browse Events**
   - Visit "Akce" page
   - Use search bar to find events: 🔍
   - Filter by: All Events, Current Events, Previous Events
   - Click event cards to see details

3. **Register for Events**
   - Click "Přihlásit se" on event cards
   - View your registrations in "Moje akce"

### For Administrators

1. **Manage Events**
   - Navigate to "Správa akcí" (Admin Events)
   - Click "➕ Vytvořit novou akci" to add events
   - Fill in: Event name, Date & time, Description
   - Edit or delete existing events

2. **Track Attendance**
   - Go to "Přihlášky" (Registrations)
   - Select an event from dropdown
   - Toggle attendance switches for each student
   - ✓ Green = Attended, ✗ Red = Not Attended

3. **View Students**
   - Visit "Studenti" page
   - See all students with event participation count
   - Click "Zobrazit akce" to see individual student's events
   - Search students by name or username

4. **Delete Events** (Safety Feature)
   - Check "🔓 Povolit mazání akcí" in deletion settings box
   - Delete buttons become active
   - Confirm deletion when prompted
   - ⚠️ Warning: Deletes all registrations and attendance records

## 🌍 Localization

The application is fully localized in Czech:

- **Akce** - Events
- **Studenti** - Students
- **Správa akcí** - Event Management
- **Přihlášky** - Registrations
- **Nadcházející akce** - Upcoming Events
- **Minulé akce** - Past Events
- **Přihlásit se** - Register
- **Odhlásit se** - Unregister
- **Zúčastněn** - Attended
- **Nezúčastněn** - Not Attended

## 🔧 Configuration

### Database
The application uses SQLite by default. Database file: `instance/school_events.db`

To use a different database, modify the `SQLALCHEMY_DATABASE_URI` in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_events.db'
```

### Secret Key
For production, set a secure secret key in `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### Date Format
Events use 24-hour time format. Minimum year: 2025.

## 📝 Scripts

### Database Management
- `rebuild_db.py` - Drop and recreate all tables (⚠️ deletes all data)
- `create_admin.py` - Create admin user account
- `add_name_field.py` - Migration script for adding name field

### Sample Data
- `create_sample_data.py` - Generate sample users
- `create_sample_previous_data.py` - Generate past events
- `generate_events.py` - Generate Czech school events
- `generate_more_events.py` - Generate additional events

## 🚦 Troubleshooting

**Database locked error**
```bash
# Stop the Flask server and run:
python rebuild_db.py
```

**Port already in use**
```bash
# Change port in app.py:
app.run(debug=True, port=5001)
```

**Authentication issues**
```bash
# Clear browser cookies or use incognito mode
# Recreate admin account:
python create_admin.py
```

**React components not loading**
- Check browser console for errors
- Verify React CDN links in templates
- Clear browser cache (Ctrl+Shift+R)
- 
## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Jakub Suchánsky** - Initial work - [myvval](https://github.com/myvval)

## 🙏 Acknowledgments

- React 18.2.0 for interactive components
- Flask for the robust backend framework
- SQLAlchemy for database ORM
- Font Awesome for icons (via emojis in this version)


## 🔮 Future Enhancements

- [ ] Email notifications for event registration
- [ ] Export attendance reports to CSV/PDF
- [ ] Calendar integration (iCal/Google Calendar)
- [ ] Event categories and tags
- [ ] Student profile photos
- [ ] Event capacity limits
- [ ] Waiting list functionality
- [ ] Multi-language support (English/Czech toggle)
- [ ] Mobile app version

---

**Made with ❤️ for SPŠD** | Last updated: October 2025
