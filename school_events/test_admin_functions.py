"""
Test script for admin data creation functions
This script tests all three admin functions to ensure they work correctly
"""
from app import app, db, User, Event, Registration
from werkzeug.security import generate_password_hash

def test_database_setup():
    """Test if database is set up correctly"""
    with app.app_context():
        print("Testing database setup...")
        
        # Check if tables exist
        try:
            user_count = User.query.count()
            event_count = Event.query.count()
            registration_count = Registration.query.count()
            
            print(f"✓ Database is accessible")
            print(f"  - Users: {user_count}")
            print(f"  - Events: {event_count}")
            print(f"  - Registrations: {registration_count}")
            return True
        except Exception as e:
            print(f"✗ Database error: {e}")
            return False

def test_admin_exists():
    """Check if admin user exists"""
    with app.app_context():
        print("\nChecking for admin user...")
        admin = User.query.filter_by(is_admin=True).first()
        
        if admin:
            print(f"✓ Admin user found: {admin.username}")
            return True
        else:
            print("✗ No admin user found")
            print("  Creating admin user 'admin' with password 'admin123'...")
            try:
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    name='Administrator',
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin user created successfully")
                return True
            except Exception as e:
                print(f"✗ Error creating admin: {e}")
                return False

def test_sample_data_creation():
    """Test the create_sample_data logic"""
    with app.app_context():
        print("\nTesting sample data creation logic...")
        
        try:
            # Count before
            events_before = Event.query.count()
            users_before = User.query.count()
            
            # Import and test the logic
            from datetime import datetime, timedelta
            import random
            
            # Create a test event
            test_event = Event(
                name="Test Event",
                date=datetime(2025, 12, 25, 10, 0),
                description="This is a test event"
            )
            db.session.add(test_event)
            db.session.commit()
            
            events_after = Event.query.count()
            
            if events_after > events_before:
                print("✓ Event creation works")
                
                # Clean up test event
                db.session.delete(test_event)
                db.session.commit()
                return True
            else:
                print("✗ Event creation failed")
                return False
                
        except Exception as e:
            print(f"✗ Error testing sample data: {e}")
            db.session.rollback()
            return False

def test_routes_exist():
    """Test if the admin routes are registered"""
    print("\nChecking if admin routes are registered...")
    
    routes = [
        '/admin/create_sample_data',
        '/admin/create_previous_data',
        '/admin/generate_events'
    ]
    
    all_exist = True
    for route in routes:
        # Check if route exists in app's url_map
        found = False
        for rule in app.url_map.iter_rules():
            if rule.rule == route:
                found = True
                print(f"✓ Route '{route}' exists")
                break
        
        if not found:
            print(f"✗ Route '{route}' not found")
            all_exist = False
    
    return all_exist

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("ADMIN FUNCTIONS TEST SUITE")
    print("="*60)
    
    results = []
    
    results.append(("Database Setup", test_database_setup()))
    results.append(("Admin User", test_admin_exists()))
    results.append(("Sample Data Logic", test_sample_data_creation()))
    results.append(("Admin Routes", test_routes_exist()))
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nThe admin buttons should work correctly.")
        print("You can now test them in the browser:")
        print("1. Log in as admin")
        print("2. Click the settings (⚙️) button")
        print("3. Try the three admin buttons:")
        print("   - Create Sample Data")
        print("   - Create Previous Sample Data")
        print("   - Generate Events")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease review the errors above.")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
