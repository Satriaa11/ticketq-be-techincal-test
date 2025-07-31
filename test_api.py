"""
Test file for TicketQ API endpoints
This file demonstrates API usage and can be used for testing
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_ticket():
    """Test creating a new ticket"""
    print("=== Testing Create Ticket ===")

    # Future date for the event
    future_date = (datetime.now() + timedelta(days=30)).isoformat()

    ticket_data = {
        "event_name": "Summer Music Festival 2024",
        "location": "Central Park, New York",
        "time": future_date
    }

    response = requests.post(
        f"{BASE_URL}/tickets",
        json=ticket_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        return response.json()["id"]
    print()

def test_get_all_tickets():
    """Test getting all tickets"""
    print("=== Testing Get All Tickets ===")
    response = requests.get(f"{BASE_URL}/tickets")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_get_specific_ticket(ticket_id):
    """Test getting a specific ticket"""
    print(f"=== Testing Get Ticket {ticket_id} ===")
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_update_ticket(ticket_id):
    """Test updating a ticket (mark as used)"""
    print(f"=== Testing Update Ticket {ticket_id} ===")

    update_data = {"is_used": True}

    response = requests.patch(
        f"{BASE_URL}/tickets/{ticket_id}",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_delete_ticket(ticket_id):
    """Test deleting a ticket"""
    print(f"=== Testing Delete Ticket {ticket_id} ===")
    response = requests.delete(f"{BASE_URL}/tickets/{ticket_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_validation_errors():
    """Test validation error handling"""
    print("=== Testing Validation Errors ===")

    # Test with missing required fields
    invalid_data = {
        "event_name": "",  # Empty event name should fail
        "location": "Test Location"
        # Missing time field
    }

    response = requests.post(
        f"{BASE_URL}/tickets",
        json=invalid_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_not_found_error():
    """Test 404 error handling"""
    print("=== Testing 404 Error ===")
    response = requests.get(f"{BASE_URL}/tickets/999")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def run_all_tests():
    """Run all tests in sequence"""
    print("Starting TicketQ API Tests...")
    print("Make sure the server is running at http://127.0.0.1:5000")
    print("=" * 50)

    try:
        # Test health check
        test_health_check()

        # Test ticket creation
        ticket_id = test_create_ticket()

        if ticket_id:
            # Test getting all tickets
            test_get_all_tickets()

            # Test getting specific ticket
            test_get_specific_ticket(ticket_id)

            # Test updating ticket
            test_update_ticket(ticket_id)

            # Test getting updated ticket
            test_get_specific_ticket(ticket_id)

            # Test deleting ticket
            test_delete_ticket(ticket_id)

            # Test getting deleted ticket (should return 404)
            test_get_specific_ticket(ticket_id)

        # Test validation errors
        test_validation_errors()

        # Test not found error
        test_not_found_error()

        print("=" * 50)
        print("All tests completed!")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running at http://127.0.0.1:5000")
        print("Run: python main.py")

if __name__ == "__main__":
    run_all_tests()
