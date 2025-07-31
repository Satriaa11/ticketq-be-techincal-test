from flask import request, jsonify
from pydantic import ValidationError
from app.services.user_service import UserService
from app.utils.auth import JWTManager
from app.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserResponseSchema,
    UserUpdateSchema,
    TokenResponseSchema,
    RefreshTokenSchema,
    ChangePasswordSchema
)
from app.schemas.ticket_schemas import ErrorResponseSchema
import math


class AuthController:
    """Controller for authentication endpoints"""

    @staticmethod
    def register():
        """POST /auth/register - Register a new user"""
        try:
            user_data = UserCreateSchema(**request.get_json())
            new_user = UserService.create_user(user_data)

            # Generate tokens
            access_token, refresh_token = UserService.generate_tokens(new_user)

            # Prepare response
            user_response = UserResponseSchema.model_validate(new_user)
            token_response = TokenResponseSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=3600,  # 1 hour
                user=user_response
            )

            return jsonify(token_response.model_dump()), 201

        except ValueError as e:
            error_response = ErrorResponseSchema(
                error="Registration Error",
                message=str(e),
                status_code=400
            )
            return jsonify(error_response.model_dump()), 400

        except ValidationError as e:
            error_response = ErrorResponseSchema(
                error="Validation Error",
                message="Invalid input data",
                status_code=400,
                details=e.errors()
            )
            return jsonify(error_response.model_dump()), 400

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500

    @staticmethod
    def login():
        """POST /auth/login - Login user"""
        try:
            login_data = UserLoginSchema(**request.get_json())
            user = UserService.authenticate_user(login_data.username, login_data.password)

            if not user:
                error_response = ErrorResponseSchema(
                    error="Authentication Error",
                    message="Invalid username or password",
                    status_code=401
                )
                return jsonify(error_response.model_dump()), 401

            # Generate tokens
            access_token, refresh_token = UserService.generate_tokens(user)

            # Prepare response
            user_response = UserResponseSchema.model_validate(user)
            token_response = TokenResponseSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=3600,  # 1 hour
                user=user_response
            )

            return jsonify(token_response.model_dump()), 200

        except ValidationError as e:
            error_response = ErrorResponseSchema(
                error="Validation Error",
                message="Invalid input data",
                status_code=400,
                details=e.errors()
            )
            return jsonify(error_response.model_dump()), 400

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500

    @staticmethod
    def refresh_token():
        """POST /auth/refresh - Refresh access token"""
        try:
            refresh_data = RefreshTokenSchema(**request.get_json())
            payload = JWTManager.decode_token(refresh_data.refresh_token)

            if 'error' in payload:
                error_response = ErrorResponseSchema(
                    error="Token Error",
                    message=payload['error'],
                    status_code=401
                )
                return jsonify(error_response.model_dump()), 401

            if payload.get('type') != 'refresh':
                error_response = ErrorResponseSchema(
                    error="Token Error",
                    message="Invalid token type",
                    status_code=401
                )
                return jsonify(error_response.model_dump()), 401

            user = UserService.get_user_by_id(payload.get('user_id'))
            if not user or not user.is_active:
                error_response = ErrorResponseSchema(
                    error="Token Error",
                    message="Invalid user",
                    status_code=401
                )
                return jsonify(error_response.model_dump()), 401

            # Generate new tokens
            access_token, new_refresh_token = UserService.generate_tokens(user)

            user_response = UserResponseSchema.model_validate(user)
            token_response = TokenResponseSchema(
                access_token=access_token,
                refresh_token=new_refresh_token,
                expires_in=3600,
                user=user_response
            )

            return jsonify(token_response.model_dump()), 200

        except ValidationError as e:
            error_response = ErrorResponseSchema(
                error="Validation Error",
                message="Invalid input data",
                status_code=400,
                details=e.errors()
            )
            return jsonify(error_response.model_dump()), 400

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500
