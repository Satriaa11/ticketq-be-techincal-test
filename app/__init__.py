from flask import Flask, jsonify, testing
from flasgger import Swagger
from app.utils.extensions import db, migrate
from app.config import Config, DevelopmentConfig, TestingConfig


def create_app(config_class=None):
    """Application factory pattern"""
    app = Flask(__name__)

    # Use config parameter or default to Config
    if config_class is None:
        config_class = Config

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Swagger
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "TicketQ API",
            "description": "Simple Ticket Management API",
            "version": "1.0.0",
            "contact": {
                "name": "TicketQ API Support",
                "email": "support@ticketq.com"
            }
        },
        "basePath": "/",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "Tickets",
                "description": "Ticket management operations"
            }
        ]
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger = Swagger(app, config=swagger_config, template=swagger_template)

    # Import models to ensure they are registered with SQLAlchemy
    from app.models import Ticket

    # Register blueprints
    from app.routes.ticket_routes import tickets_bp
    app.register_blueprint(tickets_bp)

    # Health check endpoint
    @app.route('/')
    def health_check():
        return jsonify({
            'status': 'OK',
            'message': 'TicketQ API is running',
            'version': '1.0.0',
            'documentation': '/apidocs/',
            'endpoints': {
                'tickets': '/tickets',
                'health': '/',
                'api_docs': '/apidocs/'
            },
            'database': 'SQLite',
            'architecture': {
                'pattern': 'Clean Architecture',
                'layers': ['Routes', 'Controllers', 'Services', 'Models'],
                'documentation': 'External YAML files'
            },
            'features': [
                'RESTful API',
                'Input validation with Pydantic v2',
                'External Swagger documentation',
                'Clean separation of concerns',
                'Error handling (400, 404, 500)',
                'SQLAlchemy ORM with pagination'
            ]
        })

    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'timestamp': '2025-08-01T00:00:00Z'
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal error occurred'
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Invalid request data'
        }), 400

    return app


# For backward compatibility
app = create_app()
