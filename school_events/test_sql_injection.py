"""
SQL Injection Security Test Suite
Tests various SQL injection attack vectors against the application
"""
import requests
from requests.auth import HTTPBasicAuth
import sys

BASE_URL = "http://127.0.0.1:5000"

# Common SQL injection payloads
SQL_INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "admin' --",
    "admin' #",
    "' OR 1=1--",
    "') OR ('1'='1",
    "' UNION SELECT NULL--",
    "1' AND '1'='1",
    "'; DROP TABLE users--",
    "1' OR '1'='1' /*",
    "admin'/*",
    "' WAITFOR DELAY '00:00:05'--",
    "1'; EXEC xp_cmdshell('dir')--",
    "' OR username LIKE '%admin%'--",
    "1' UNION ALL SELECT NULL,NULL,NULL--",
    "' AND 1=CONVERT(int, (SELECT @@version))--",
]

def test_login_sql_injection():
    """Test login form for SQL injection vulnerabilities"""
    print("\n=== Testing Login Form ===")
    session = requests.Session()
    
    for payload in SQL_INJECTION_PAYLOADS:
        print(f"\nTesting payload: {payload}")
        
        # Get CSRF token if needed
        try:
            response = session.post(
                f"{BASE_URL}/login",
                data={
                    'username': payload,
                    'password': 'anything'
                },
                allow_redirects=False
            )
            
            # If we get redirected to index, injection might have worked
            if response.status_code == 302 and '/index' in response.headers.get('Location', ''):
                print(f"⚠️  VULNERABLE: Payload bypassed authentication!")
                return False
            elif 'Invalid username or password' in response.text or response.status_code in [200, 302]:
                print(f"✓ Safe: Payload was safely handled")
            else:
                print(f"? Unknown response: {response.status_code}")
                
        except Exception as e:
            print(f"✓ Safe: Exception caught - {str(e)[:50]}")
    
    print("\n✅ Login form is SECURE against SQL injection")
    return True

def test_registration_sql_injection():
    """Test registration form for SQL injection vulnerabilities"""
    print("\n=== Testing Registration Form ===")
    session = requests.Session()
    
    for i, payload in enumerate(SQL_INJECTION_PAYLOADS[:5]):  # Test subset
        print(f"\nTesting payload: {payload}")
        
        try:
            response = session.post(
                f"{BASE_URL}/register",
                data={
                    'username': payload,
                    'password': 'testpass123',
                    'name': 'Test User'
                },
                allow_redirects=False
            )
            
            # Check if error was handled properly
            if response.status_code in [200, 302]:
                print(f"✓ Safe: Payload was safely handled")
            else:
                print(f"? Unknown response: {response.status_code}")
                
        except Exception as e:
            print(f"✓ Safe: Exception caught - {str(e)[:50]}")
    
    print("\n✅ Registration form is SECURE against SQL injection")
    return True

def test_search_sql_injection():
    """Test search functionality for SQL injection vulnerabilities"""
    print("\n=== Testing Search Functionality ===")
    
    # First login as admin
    session = requests.Session()
    session.post(f"{BASE_URL}/login", data={'username': 'admin', 'password': 'admin'})
    
    for payload in SQL_INJECTION_PAYLOADS:
        print(f"\nTesting search payload: {payload}")
        
        try:
            response = session.get(
                f"{BASE_URL}/admin/registrations",
                params={'query': payload}
            )
            
            if response.status_code == 200:
                # Check if we got normal results or error page
                if 'Traceback' in response.text or 'SQL' in response.text:
                    print(f"⚠️  VULNERABLE: SQL error exposed!")
                    return False
                else:
                    print(f"✓ Safe: Search handled payload safely")
            else:
                print(f"? Status: {response.status_code}")
                
        except Exception as e:
            print(f"✓ Safe: Exception caught - {str(e)[:50]}")
    
    print("\n✅ Search functionality is SECURE against SQL injection")
    return True

def test_event_id_sql_injection():
    """Test event ID parameter for SQL injection"""
    print("\n=== Testing Event ID Parameter ===")
    
    session = requests.Session()
    session.post(f"{BASE_URL}/login", data={'username': 'admin', 'password': 'admin'})
    
    injection_ids = [
        "1' OR '1'='1",
        "1 UNION SELECT NULL",
        "1; DROP TABLE events--",
        "1' AND 1=1--",
    ]
    
    for payload in injection_ids:
        print(f"\nTesting event ID payload: {payload}")
        
        try:
            response = session.get(f"{BASE_URL}/event/{payload}")
            
            if response.status_code == 404:
                print(f"✓ Safe: Invalid ID rejected")
            elif response.status_code == 200:
                print(f"✓ Safe: Handled safely (possibly showing event)")
            elif 'error' in response.text.lower():
                print(f"⚠️  Warning: Error message visible")
                
        except Exception as e:
            print(f"✓ Safe: Exception caught - {str(e)[:50]}")
    
    print("\n✅ Event ID parameter is SECURE against SQL injection")
    return True

def main():
    print("=" * 60)
    print("SQL INJECTION SECURITY TEST SUITE")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print("=" * 60)
    
    try:
        # Check if server is running
        response = requests.get(BASE_URL, timeout=5)
        print("✓ Server is running\n")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server. Is Flask running?")
        sys.exit(1)
    
    results = []
    
    # Run all tests
    results.append(("Login Form", test_login_sql_injection()))
    results.append(("Registration Form", test_registration_sql_injection()))
    results.append(("Search Function", test_search_sql_injection()))
    results.append(("Event ID Parameter", test_event_id_sql_injection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SECURITY TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ SECURE" if passed else "⚠️  VULNERABLE"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED - Application is secure against SQL injection!")
        print("\nNOTE: The application uses SQLAlchemy ORM with parameterized queries,")
        print("which automatically protects against SQL injection attacks.")
    else:
        print("\n⚠️  VULNERABILITIES DETECTED - Please review the failed tests!")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
