# TicketQ Backend API

A Flask-based REST API for ticket management system with Pydantic v2 validation, user authentication, and role-based access control.

## Features

- ✅ Complete CRUD operations for tickets
- ✅ User authentication and authorization (JWT tokens)
- ✅ Role-based access control (Admin/User roles)
- ✅ Pydantic v2 validation with comprehensive error handling
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Input validation (required fields, time validation, password strength, etc.)
- ✅ Error handling (404, 400, 401, 403, 500)
- ✅ Pagination support
- ✅ Clean architecture with separation of concerns

## User Roles & Permissions

### Admin Role

- Can view all tickets
- Can create tickets
- Can update any ticket status
- Can delete any ticket
- Can manage users (view, update, delete)
- Can access user management endpoints

### User Role

- Can view all tickets (public information)
- Can create tickets
- Can only update their own tickets
- Cannot delete tickets
- Can manage their own profile
- Cannot access admin endpoints

### Anonymous (No Authentication)

- Can view tickets (public information)
- Can view specific ticket details
- Cannot create, update, or delete tickets
- Cannot access user endpoints

## Requirements

- Python 3.11+
- Flask
- Pydantic v2 with email-validator
- SQLAlchemy
- Flask-Migrate
- PyJWT
- bcrypt

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ticketq-be-techincal-test
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
uv sync
# or
pip install -r requirements.txt
```

4. Set up the database:

```bash
python setup_db.py
```

This will create the database tables and a default admin user:

- Username: `admin`
- Password: `Admin123!`
- Email: `admin@ticketq.com`

## Running the Application

```bash
python main.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### Health Check

- **GET** `/` - API health check
- **GET** `/health` - Detailed health check

### Authentication

#### 1. Register New User

- **POST** `/auth/register`
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "role": "user"
}
```

**Response (201):**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-07-31T10:00:00",
    "updated_at": "2024-07-31T10:00:00"
  }
}
```

#### 2. Login User

- **POST** `/auth/login`
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response (200):** Same as registration response

#### 3. Refresh Token

- **POST** `/auth/refresh`
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):** Returns new access and refresh tokens

### User Management

#### 1. Get Current User Profile

- **GET** `/users/me`
- **Authorization**: Bearer token required

**Response (200):**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-07-31T10:00:00",
  "updated_at": "2024-07-31T10:00:00"
}
```

#### 2. Update Current User Profile

- **PUT** `/users/me`
- **Authorization**: Bearer token required
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "email": "newemail@example.com",
  "full_name": "John Updated Doe"
}
```

#### 3. Change Password

- **POST** `/users/me/change-password`
- **Authorization**: Bearer token required
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "current_password": "OldPass123!",
  "new_password": "NewSecurePass123!"
}
```

#### 4. Get All Users (Admin Only)

- **GET** `/users`
- **Authorization**: Bearer token required (Admin role)
- **Query Parameters**:
  - `page` (optional): Page number (default: 1)
  - `per_page` (optional): Items per page (default: 10, max: 100)

#### 5. Get User by ID (Admin Only)

- **GET** `/users/{user_id}`
- **Authorization**: Bearer token required (Admin role)

#### 6. Update User (Admin Only)

- **PUT** `/users/{user_id}`
- **Authorization**: Bearer token required (Admin role)
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "email": "updated@example.com",
  "full_name": "Updated Name",
  "role": "admin",
  "is_active": false
}
```

#### 7. Delete User (Admin Only)

- **DELETE** `/users/{user_id}`
- **Authorization**: Bearer token required (Admin role)

### Ticket Management

#### 1. Create a New Ticket

- **POST** `/tickets`
- **Authorization**: Bearer token required
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "event_name": "Concert 2024",
  "location": "Madison Square Garden",
  "time": "2024-12-31T20:00:00"
}
```

**Response (201):**

```json
{
  "id": 1,
  "event_name": "Concert 2024",
  "location": "Madison Square Garden",
  "time": "2024-12-31T20:00:00",
  "is_used": false,
  "created_by_id": 1,
  "created_at": "2024-07-31T10:00:00",
  "updated_at": "2024-07-31T10:00:00"
}
```

```json
{
  "id": 1,
  "event_name": "Concert 2024",
  "location": "Madison Square Garden",
  "time": "2024-12-31T20:00:00",
  "is_used": false,
  "created_at": "2024-07-31T10:00:00",
  "updated_at": "2024-07-31T10:00:00"
}
```

#### 2. List All Tickets

- **GET** `/tickets`
- **Query Parameters**:
  - `page` (optional): Page number (default: 1)
  - `per_page` (optional): Items per page (default: 10, max: 100)

**Response (200):**

```json
{
  "tickets": [
    {
      "id": 1,
      "event_name": "Concert 2024",
      "location": "Madison Square Garden",
      "time": "2024-12-31T20:00:00",
      "is_used": false,
      "created_at": "2024-07-31T10:00:00",
      "updated_at": "2024-07-31T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "total_pages": 1
}
```

#### 3. Get Specific Ticket

- **GET** `/tickets/{id}`

**Response (200):**

```json
{
  "id": 1,
  "event_name": "Concert 2024",
  "location": "Madison Square Garden",
  "time": "2024-12-31T20:00:00",
  "is_used": false,
  "created_at": "2024-07-31T10:00:00",
  "updated_at": "2024-07-31T10:00:00"
}
```

#### 4. Mark Ticket as Used

- **PATCH** `/tickets/{id}`
- **Content-Type**: `application/json`

**Request Body:**

```json
{
  "is_used": true
}
```

**Response (200):**

```json
{
  "id": 1,
  "event_name": "Concert 2024",
  "location": "Madison Square Garden",
  "time": "2024-12-31T20:00:00",
  "is_used": true,
  "created_at": "2024-07-31T10:00:00",
  "updated_at": "2024-07-31T10:15:00"
}
```

#### 5. Delete Ticket

- **DELETE** `/tickets/{id}`

**Response (200):**

```json
{
  "message": "Ticket 1 deleted successfully"
}
```

## Error Handling

### Validation Errors (400)

```json
{
  "error": "Validation Error",
  "message": "Invalid input data",
  "status_code": 400,
  "details": [
    {
      "type": "missing",
      "loc": ["event_name"],
      "msg": "Field required"
    }
  ]
}
```

### Not Found (404)

```json
{
  "error": "Not Found",
  "message": "Ticket with ID 999 not found",
  "status_code": 404
}
```

### Internal Server Error (500)

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "status_code": 500
}
```

## Validation Rules

### Ticket Creation

- `event_name`: Required, 1-255 characters, cannot be empty or whitespace
- `location`: Required, 1-255 characters, cannot be empty or whitespace
- `time`: Required, valid ISO datetime format, cannot be in the past

### Ticket Update

- `is_used`: Required boolean value

## Project Structure

```
ticketq-be-techincal-test/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── controllers/         # Request handlers
│   │   ├── __init__.py
│   │   └── ticket_controller.py
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── ticket.py
│   ├── routes/              # URL routing
│   │   ├── __init__.py
│   │   └── ticket_routes.py
│   ├── schemas/             # Pydantic validation schemas
│   │   ├── __init__.py
│   │   └── ticket_schemas.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── ticket_service.py
│   └── utils/               # Utilities and extensions
│       ├── __init__.py
│       └── extensions.py
├── main.py                  # Application entry point
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Testing with cURL

### Create a ticket:

```bash
curl -X POST http://127.0.0.1:5000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "Summer Music Festival",
    "location": "Central Park",
    "time": "2024-08-15T18:00:00"
  }'
```

### Get all tickets:

```bash
curl http://127.0.0.1:5000/tickets
```

### Get specific ticket:

```bash
curl http://127.0.0.1:5000/tickets/1
```

### Mark ticket as used:

```bash
curl -X PATCH http://127.0.0.1:5000/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"is_used": true}'
```

### Delete ticket:

```bash
curl -X DELETE http://127.0.0.1:5000/tickets/1
```

## Development

The application uses Flask's development server. For production deployment, consider using a WSGI server like Gunicorn.

### Database Migrations

The application uses Flask-Migrate for database migrations:

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Create tickets table"

# Apply migrations
flask db upgrade
```

## License

This project is created for technical assessment purposes.
