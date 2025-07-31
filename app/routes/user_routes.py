from flask import Blueprint
from app.controllers.user_controller import UserController

# Create users blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# Define routes
users_bp.route('/me', methods=['GET'])(UserController.get_current_user)
users_bp.route('/me', methods=['PUT'])(UserController.update_current_user)
users_bp.route('/me/change-password', methods=['POST'])(UserController.change_password)

# Admin routes
users_bp.route('/', methods=['GET'])(UserController.get_all_users)
users_bp.route('/<int:user_id>', methods=['GET'])(UserController.get_user_by_id)
users_bp.route('/<int:user_id>', methods=['PUT'])(UserController.update_user)
users_bp.route('/<int:user_id>', methods=['DELETE'])(UserController.delete_user)
