from .ticket_routes import tickets_bp
from .auth_routes import auth_bp
from .user_routes import users_bp

__all__ = ['tickets_bp', 'auth_bp', 'users_bp']
