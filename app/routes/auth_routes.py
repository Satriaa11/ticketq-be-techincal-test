from flask import Blueprint
from app.controllers.auth_controller import AuthController

# Create auth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Define routes
auth_bp.route('/register', methods=['POST'])(AuthController.register)
auth_bp.route('/login', methods=['POST'])(AuthController.login)
auth_bp.route('/refresh', methods=['POST'])(AuthController.refresh_token)
