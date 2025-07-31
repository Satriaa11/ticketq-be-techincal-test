import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from app.models.user import User
from app.schemas.user_schemas import UserRole


class JWTManager:
    """JWT token management utility"""

    @staticmethod
    def generate_tokens(user):
        """Generate access and refresh tokens for user"""
        access_payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'access'
        }

        refresh_payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }

        access_token = jwt.encode(
            access_payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )

        refresh_token = jwt.encode(
            refresh_payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )

        return access_token, refresh_token

    @staticmethod
    def decode_token(token):
        """Decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}

    @staticmethod
    def get_current_user_from_token():
        """Get current user from JWT token"""
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return None

        if not token:
            return None

        payload = JWTManager.decode_token(token)
        if 'error' in payload:
            return None

        if payload.get('type') != 'access':
            return None

        user = User.query.get(payload.get('user_id'))
        return user if user and user.is_active else None


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = JWTManager.get_current_user_from_token()
        if user is None:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Valid token is required to access this resource',
                'status_code': 401
            }), 401

        return f(current_user=user, *args, **kwargs)
    return decorated


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = JWTManager.get_current_user_from_token()
        if user is None:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Valid token is required to access this resource',
                'status_code': 401
            }), 401

        if not user.is_admin():
            return jsonify({
                'error': 'Forbidden',
                'message': 'Admin access required',
                'status_code': 403
            }), 403

        return f(current_user=user, *args, **kwargs)
    return decorated


def optional_auth(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = JWTManager.get_current_user_from_token()
        return f(current_user=user, *args, **kwargs)
    return decorated
