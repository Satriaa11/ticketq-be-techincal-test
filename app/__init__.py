from flask import Flask, jsonify
from app.utils.extensions import db, migrate
from app.config import Config


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

    # Import models to ensure they are registered with SQLAlchemy
    from app.models import Ticket, User

    # Register blueprints
    from app.routes.ticket_routes import tickets_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import users_bp

    app.register_blueprint(tickets_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    # Health check endpoint
    @app.route('/')
    def health_check():
        return jsonify({
            'status': 'OK',
            'message': 'TicketQ API is running',
            'version': '1.0.0',
            'endpoints': {
                'tickets': '/tickets',
                'auth': '/auth',
                'users': '/users',
                'health': '/health'
            },
            'authentication': {
                'register': 'POST /auth/register',
                'login': 'POST /auth/login',
                'refresh': 'POST /auth/refresh'
            }
        })

    @app.route('/health')
    def api_health():
        """API Health check"""
        return jsonify({
            'status': 'OK',
            'message': 'TicketQ API is running',
            'version': '1.0.0'
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500

    return app


# For backward compatibility
app = create_app()
