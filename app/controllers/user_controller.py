from flask import request, jsonify
from pydantic import ValidationError
from app.services.user_service import UserService
from app.utils.auth import token_required, admin_required
from app.schemas.user_schemas import (
    UserResponseSchema,
    UserUpdateSchema,
    ChangePasswordSchema
)
from app.schemas.ticket_schemas import ErrorResponseSchema
import math


class UserController:
    """Controller for user management endpoints"""

    @staticmethod
    @token_required
    def get_current_user(current_user):
        """GET /users/me - Get current user profile"""
        try:
            user_response = UserResponseSchema.model_validate(current_user)
            return jsonify(user_response.model_dump()), 200

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500

    @staticmethod
    @token_required
    def update_current_user(current_user):
        """PUT /users/me - Update current user profile"""
        try:
            update_data = UserUpdateSchema(**request.get_json())

            # Users can only update their own email and full_name
            limited_update = UserUpdateSchema(
                email=update_data.email,
                full_name=update_data.full_name
            )

            updated_user = UserService.update_user(current_user.id, limited_update)
            if not updated_user:
                error_response = ErrorResponseSchema(
                    error="Not Found",
                    message="User not found",
                    status_code=404
                )
                return jsonify(error_response.model_dump()), 404

            user_response = UserResponseSchema.model_validate(updated_user)
            return jsonify(user_response.model_dump()), 200

        except ValueError as e:
            error_response = ErrorResponseSchema(
                error="Update Error",
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
    @token_required
    def change_password(current_user):
        """POST /users/me/change-password - Change current user password"""
        try:
            password_data = ChangePasswordSchema(**request.get_json())
            success = UserService.change_password(current_user.id, password_data)

            if not success:
                error_response = ErrorResponseSchema(
                    error="Password Change Error",
                    message="Failed to change password",
                    status_code=400
                )
                return jsonify(error_response.model_dump()), 400

            return jsonify({"message": "Password changed successfully"}), 200

        except ValueError as e:
            error_response = ErrorResponseSchema(
                error="Password Change Error",
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
    @admin_required
    def get_all_users(current_user):
        """GET /users - Get all users (Admin only)"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)

            users, total = UserService.get_all_users(page, per_page)
            total_pages = math.ceil(total / per_page)

            user_responses = [UserResponseSchema.model_validate(user) for user in users]

            response_data = {
                "users": [user.model_dump() for user in user_responses],
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages
            }

            return jsonify(response_data), 200

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500

    @staticmethod
    @admin_required
    def get_user_by_id(current_user, user_id):
        """GET /users/:id - Get user by ID (Admin only)"""
        try:
            user = UserService.get_user_by_id(user_id)
            if not user:
                error_response = ErrorResponseSchema(
                    error="Not Found",
                    message=f"User with ID {user_id} not found",
                    status_code=404
                )
                return jsonify(error_response.model_dump()), 404

            user_response = UserResponseSchema.model_validate(user)
            return jsonify(user_response.model_dump()), 200

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500

    @staticmethod
    @admin_required
    def update_user(current_user, user_id):
        """PUT /users/:id - Update user (Admin only)"""
        try:
            update_data = UserUpdateSchema(**request.get_json())
            updated_user = UserService.update_user(user_id, update_data)

            if not updated_user:
                error_response = ErrorResponseSchema(
                    error="Not Found",
                    message=f"User with ID {user_id} not found",
                    status_code=404
                )
                return jsonify(error_response.model_dump()), 404

            user_response = UserResponseSchema.model_validate(updated_user)
            return jsonify(user_response.model_dump()), 200

        except ValueError as e:
            error_response = ErrorResponseSchema(
                error="Update Error",
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
    @admin_required
    def delete_user(current_user, user_id):
        """DELETE /users/:id - Delete user (Admin only)"""
        try:
            # Prevent admin from deleting themselves
            if current_user.id == user_id:
                error_response = ErrorResponseSchema(
                    error="Forbidden",
                    message="Cannot delete your own account",
                    status_code=403
                )
                return jsonify(error_response.model_dump()), 403

            deleted = UserService.delete_user(user_id)
            if not deleted:
                error_response = ErrorResponseSchema(
                    error="Not Found",
                    message=f"User with ID {user_id} not found",
                    status_code=404
                )
                return jsonify(error_response.model_dump()), 404

            return jsonify({"message": f"User {user_id} deleted successfully"}), 200

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500
