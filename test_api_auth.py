#!/usr/bin/env python3
"""
Test script for TicketQ API with User Authentication and Authorization
This script demonstrates all API endpoints with proper authentication.
"""

import requests
import json
from datetime import datetime, timedelta
import sys


# API Configuration
BASE_URL = "http://127.0.0.1:5000"
HEADERS = {"Content-Type": "application/json"}


def print_response(response, operation):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"OPERATION: {operation}")
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print('='*50)


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Health Check")
    return response.status_code == 200


def test_user_registration():
    """Test user registration"""
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "SecurePass123!",
        "full_name": "John Doe",
        "role": "user"
    }

    response = requests.post(f"{BASE_URL}/auth/register",
                           headers=HEADERS,
                           json=user_data)
    print_response(response, "User Registration")

    if response.status_code == 201:
        return response.json()
    return None


def test_admin_login():
    """Test admin login"""
    login_data = {
        "username": "admin",
        "password": "Admin123!"
    }

    response = requests.post(f"{BASE_URL}/auth/login",
                           headers=HEADERS,
                           json=login_data)
    print_response(response, "Admin Login")

    if response.status_code == 200:
        return response.json()
    return None


def test_user_login():
    """Test regular user login"""
    login_data = {
        "username": "johndoe",
        "password": "SecurePass123!"
    }

    response = requests.post(f"{BASE_URL}/auth/login",
                           headers=HEADERS,
                           json=login_data)
    print_response(response, "User Login")

    if response.status_code == 200:
        return response.json()
    return None


def test_create_ticket(token):
    """Test creating a ticket (requires authentication)"""
    auth_headers = {
        **HEADERS,
        "Authorization": f"Bearer {token}"
    }

    # Create event time for tomorrow
    event_time = (datetime.now() + timedelta(days=1)).isoformat()

    ticket_data = {
        "event_name": "Tech Conference 2025",
        "location": "Jakarta Convention Center",
        "time": event_time
    }

    response = requests.post(f"{BASE_URL}/tickets",
                           headers=auth_headers,
                           json=ticket_data)
    print_response(response, "Create Ticket (Authenticated)")

    if response.status_code == 201:
        return response.json()
    return None


def test_get_all_tickets(token=None):
    """Test getting all tickets (optional authentication)"""
    headers = HEADERS
    if token:
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/tickets", headers=headers)
    print_response(response, f"Get All Tickets ({'Authenticated' if token else 'Anonymous'})")
    return response.status_code == 200


def test_get_ticket_by_id(ticket_id, token=None):
    """Test getting a specific ticket"""
    headers = HEADERS
    if token:
        headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}", headers=headers)
    print_response(response, f"Get Ticket by ID ({ticket_id})")
    return response.status_code == 200


def test_update_ticket_status(ticket_id, token, is_used=True):
    """Test updating ticket status (requires authentication)"""
    auth_headers = {
        **HEADERS,
        "Authorization": f"Bearer {token}"
    }

    update_data = {
        "is_used": is_used
    }

    response = requests.patch(f"{BASE_URL}/tickets/{ticket_id}",
                            headers=auth_headers,
                            json=update_data)
    print_response(response, f"Update Ticket Status (Mark as {'Used' if is_used else 'Unused'})")
    return response.status_code == 200


def test_get_current_user(token):
    """Test getting current user profile"""
    auth_headers = {
        **HEADERS,
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/users/me", headers=auth_headers)
    print_response(response, "Get Current User Profile")
    return response.status_code == 200


def test_get_all_users_admin(admin_token):
    """Test getting all users (admin only)"""
    auth_headers = {
        **HEADERS,
        "Authorization": f"Bearer {admin_token}"
    }

    response = requests.get(f"{BASE_URL}/users", headers=auth_headers)
    print_response(response, "Get All Users (Admin Only)")
    return response.status_code == 200


def test_delete_ticket_admin(ticket_id, admin_token):
    """Test deleting ticket (admin only)"""
    auth_headers = {
        **HEADERS,
        "Authorization": f"Bearer {admin_token}"
    }

    response = requests.delete(f"{BASE_URL}/tickets/{ticket_id}", headers=auth_headers)
    print_response(response, "Delete Ticket (Admin Only)")
    return response.status_code == 200


def test_unauthorized_access():
    """Test unauthorized access to protected endpoints"""
    print(f"\n{'='*50}")
    print("TESTING UNAUTHORIZED ACCESS")
    print('='*50)

    # Try to create ticket without authentication
    ticket_data = {
        "event_name": "Unauthorized Event",
        "location": "Nowhere",
        "time": (datetime.now() + timedelta(days=1)).isoformat()
    }

    response = requests.post(f"{BASE_URL}/tickets",
                           headers=HEADERS,
                           json=ticket_data)
    print_response(response, "Create Ticket (No Auth) - Should Fail")

    # Try to access admin endpoint as regular user
    # This will be tested later in the main function


def main():
    """Main test function"""
    print("🚀 Starting TicketQ API Tests with Authentication")
    print("="*60)

    # Health check
    if not test_health_check():
        print("❌ Health check failed!")
        return

    print("\n📋 TESTING USER REGISTRATION & AUTHENTICATION")

    # Register a new user
    user_registration = test_user_registration()
    if not user_registration:
        print("❌ User registration failed!")
        return

    user_token = user_registration["access_token"]
    user_data = user_registration["user"]

    # Login as admin
    admin_login = test_admin_login()
    if not admin_login:
        print("❌ Admin login failed!")
        return

    admin_token = admin_login["access_token"]

    # Login as regular user (alternative way)
    user_login = test_user_login()
    if user_login:
        user_token = user_login["access_token"]  # Use fresh token

    print("\n🎫 TESTING TICKET OPERATIONS")

    # Test creating tickets
    ticket1 = test_create_ticket(user_token)
    ticket2 = test_create_ticket(admin_token)

    if not ticket1:
        print("❌ Ticket creation failed!")
        return

    ticket_id = ticket1["id"]

    # Test getting all tickets (anonymous)
    test_get_all_tickets()

    # Test getting all tickets (authenticated)
    test_get_all_tickets(user_token)

    # Test getting specific ticket
    test_get_ticket_by_id(ticket_id)
    test_get_ticket_by_id(ticket_id, user_token)

    # Test updating ticket status
    test_update_ticket_status(ticket_id, user_token, True)

    print("\n👤 TESTING USER OPERATIONS")

    # Test getting current user profile
    test_get_current_user(user_token)
    test_get_current_user(admin_token)

    # Test admin operations
    test_get_all_users_admin(admin_token)

    print("\n🔒 TESTING AUTHORIZATION")

    # Test unauthorized access
    test_unauthorized_access()

    # Try admin operation as regular user
    auth_headers = {
        **HEADERS,
        "Authorization": f"Bearer {user_token}"
    }

    response = requests.get(f"{BASE_URL}/users", headers=auth_headers)
    print_response(response, "Get All Users (Regular User) - Should Fail")

    # Test admin deleting ticket
    if ticket2:
        test_delete_ticket_admin(ticket2["id"], admin_token)

    print("\n✅ TESTING COMPLETED!")
    print("\nKEY FEATURES DEMONSTRATED:")
    print("✓ User registration and authentication")
    print("✓ Role-based access control (Admin vs User)")
    print("✓ JWT token-based authentication")
    print("✓ Protected and public endpoints")
    print("✓ Proper error handling and validation")
    print("✓ Ticket ownership and permissions")

    print(f"\n📖 API DOCUMENTATION:")
    print(f"Health Check: GET {BASE_URL}/")
    print(f"Register: POST {BASE_URL}/auth/register")
    print(f"Login: POST {BASE_URL}/auth/login")
    print(f"Tickets: GET/POST {BASE_URL}/tickets")
    print(f"User Profile: GET {BASE_URL}/users/me")
    print(f"Admin Panel: GET {BASE_URL}/users (Admin only)")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server!")
        print("Make sure the server is running on http://127.0.0.1:5000")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
        sys.exit(0)
