# 🎫 TicketQ - Event Ticket Management API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)](https://sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A simple and clean REST API for managing event tickets built with Flask, SQLAlchemy, and modern Python practices.

## 🚀 Features

- ✅ **RESTful API** - Complete CRUD operations for tickets
<!-- - ✅ **Clean Architecture** - Separation of concerns with layered structure -->
- ✅ **Input Validation** - Pydantic v2 for robust data validation
- ✅ **API Documentation** - Interactive Swagger UI documentation
- ✅ **Database Support** - SQLite for development, PostgreSQL ready for production
- ✅ **Environment Configuration** - Flexible configuration management
- ✅ **Error Handling** - Comprehensive error responses (400, 404, 500)
- ✅ **Pagination** - Efficient data retrieval with pagination support

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Database Management](#-database-management)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## 🏃 Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Satriaa11/ticketq-be-techincal-test.git
   cd ticketq-be-techincal-test
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env file with your configurations
   ```

4. **Initialize database**

   ```bash
   # Simple database setup
   uv run python -c "from app import create_app; from app.utils.extensions import db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
   ```

5. **Start the server**

   ```bash
   uv run flask run
   ```

6. **Access the application**
   - API: http://localhost:5000
   - Swagger Documentation: http://localhost:5000/apidocs/

## 🔗 API Endpoints

### Base URL: `http://localhost:5000`

| Method   | Endpoint        | Description                 | Request Body                   |
| -------- | --------------- | --------------------------- | ------------------------------ |
| `GET`    | `/`             | Health check and API info   | -                              |
| `GET`    | `/health`       | Simple health status        | -                              |
| `GET`    | `/tickets`      | Get all tickets (paginated) | -                              |
| `GET`    | `/tickets/{id}` | Get specific ticket         | -                              |
| `POST`   | `/tickets`      | Create new ticket           | [TicketCreate](#ticket-schema) |
| `PATCH`  | `/tickets/{id}` | Mark ticket as used/unused  | [TicketUpdate](#ticket-schema) |
| `DELETE` | `/tickets/{id}` | Delete ticket               | -                              |

### 📝 Ticket Schema

#### Create/Update Request

```json
{
  "eventName": "Tech Conference 2025",
  "location": "Jakarta Convention Center",
  "time": "2025-08-15T10:00:00"
}
```

#### Response

```json
{
  "id": 1,
  "eventName": "Tech Conference 2025",
  "location": "Jakarta Convention Center",
  "time": "2025-08-15T10:00:00",
  "isUsed": false,
  "createdAt": "2025-08-01T12:00:00",
  "updatedAt": "2025-08-01T12:00:00"
}
```

### 📄 Pagination Response

```json
{
  "tickets": [...],
  "pagination": {
    "page": 1,
    "pages": 3,
    "per_page": 10,
    "total": 25,
    "has_next": true,
    "has_prev": false
  }
}
```

## 📁 Project Structure

```
ticketq-be-techincal-test/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration classes
│   ├── controllers/             # Business logic layer
│   │   └── ticket_controller.py
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   └── ticket.py
│   ├── routes/                  # API route definitions
│   │   └── ticket_routes.py
│   ├── schemas/                 # Pydantic validation schemas
│   │   └── ticket_schemas.py
│   ├── services/                # Service layer
│   │   └── ticket_service.py
│   ├── utils/                   # Utilities and extensions
│   │   ├── __init__.py
│   │   └── extensions.py
│   └── docs/                    # API documentation
│       └── swagger/
├── migrations/                  # Database migrations
├── create_db.py                 # Database initialization script
├── db_manager.py               # Database management utility
├── main.py                     # Application entry point
├── .env                        # Environment variables
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```properties
# Flask Configuration
FLASK_APP=app:create_app
FLASK_DEBUG=1
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=0.0.0.0

# Application Environment
ENV=development

# Database Configuration
DATABASE_URL=sqlite:///tickets_dev.db

# Security
SECRET_KEY=your-secret-key-here

# API Configuration
API_TITLE=TicketQ API
API_VERSION=1.0.0
```

### Configuration Classes

- **DevelopmentConfig**: For local development
- **TestingConfig**: For running tests
- **ProductionConfig**: For production deployment

Switch between configurations using the `ENV` environment variable.

<!-- ## 🗄️ Database Management

### Initialize Database

```bash
# Create database and tables
uv run python -c "from app import create_app; from app.utils.extensions import db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### Database Operations

```bash
# Check database with Python
uv run python -c "from app import create_app; from app.models.ticket import Ticket; app = create_app(); app.app_context().push(); print(f'Total tickets: {Ticket.query.count()}')"

# Add sample ticket
uv run python -c "
from app import create_app
from app.utils.extensions import db
from app.models.ticket import Ticket
from datetime import datetime

app = create_app()
app.app_context().push()

ticket = Ticket(
    event_name='Sample Event',
    location='Sample Location',
    time=datetime(2025, 8, 15, 10, 0, 0)
)
db.session.add(ticket)
db.session.commit()
print('Sample ticket added!')
"
``` -->

### Migration Commands

```bash
# Initialize migrations (first time only)
uv run flask db init

# Create new migration
uv run flask db migrate -m "Description of changes"

# Apply migrations
uv run flask db upgrade
```

## 🛠️ Development

### Running in Development Mode

```bash
# Start with auto-reload
uv run flask run --debug

# Or with environment variables
ENV=development uv run flask run
```

<!-- ### Code Style and Quality

```bash
# Format code (if using black)
black app/

# Lint code (if using flake8)
flake8 app/

# Type checking (if using mypy)
mypy app/
``` -->

### Development Tools

- **Flask-CORS**: Cross-origin resource sharing
- **Flask-Migrate**: Database migrations
- **Flasgger**: Swagger documentation generation
- **python-dotenv**: Environment variable management

## 🧪 Testing

### Run Tests

<!-- ```bash
# Run all tests
ENV=testing uv run python -m pytest

# Run with coverage
ENV=testing uv run python -m pytest --cov=app

# Run specific test file
ENV=testing uv run python -m pytest tests/test_tickets.py
``` -->

### Test API Endpoints

```bash
# Test with curl
curl -X GET http://localhost:5000/tickets

# Test create ticket
curl -X POST http://localhost:5000/tickets \
  -H "Content-Type: application/json" \
  -d '{"eventName":"Test Event","location":"Test Location","time":"2025-08-15T10:00:00"}'
```

## 🚀 Deployment

### Production Setup

1. **Set environment variables**

   ```bash
   export ENV=production
   export DATABASE_URL=postgresql://user:pass@localhost/ticketq
   export SECRET_KEY=your-production-secret-key
   ```

2. **Install production dependencies**

   ```bash
   uv sync --no-dev
   ```

3. **Run with production server**

   ```bash
   # Using Gunicorn
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

   # Using uWSGI
   pip install uwsgi
   uwsgi --http :5000 --module app:create_app()
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync --no-dev

EXPOSE 5000
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Swagger/OpenAPI Specification](https://swagger.io/docs/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Satria Aditama**

- GitHub: [@Satriaa11](https://github.com/Satriaa11)
- Project: [TicketQ Backend Technical Test](https://github.com/Satriaa11/ticketq-be-techincal-test)

---

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Satriaa11/ticketq-be-techincal-test/issues) page
2. Create a new issue with detailed information
3. Include logs and error messages if applicable

**Made with ❤️ for RevoU Bootcamp Technical Assessment**
