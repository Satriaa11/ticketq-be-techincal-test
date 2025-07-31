from typing import Optional, List, Tuple
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.user import User
from app.utils.extensions import db
from app.schemas.user_schemas import UserCreateSchema, UserUpdateSchema, ChangePasswordSchema
from app.utils.auth import JWTManager


class UserService:
    """Service layer for user operations"""

    @staticmethod
    def create_user(user_data: UserCreateSchema) -> User:
        """Create a new user"""
        try:
            # Check if username or email already exists
            if User.query.filter_by(username=user_data.username).first():
                raise ValueError("Username already exists")

            if User.query.filter_by(email=user_data.email).first():
                raise ValueError("Email already exists")

            new_user = User(
                username=user_data.username,
                email=user_data.email,
                full_name=user_data.full_name,
                role=user_data.role
            )
            new_user.set_password(user_data.password)

            db.session.add(new_user)
            db.session.commit()
            return new_user

        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username or email already exists")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to create user: {str(e)}")

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        try:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password) and user.is_active:
                return user
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Authentication failed: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve user: {str(e)}")

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        try:
            return User.query.filter_by(username=username).first()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve user: {str(e)}")

    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 10) -> Tuple[List[User], int]:
        """Get all users with pagination"""
        try:
            pagination = User.query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            return pagination.items, pagination.total
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve users: {str(e)}")

    @staticmethod
    def update_user(user_id: int, update_data: UserUpdateSchema) -> Optional[User]:
        """Update user information"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None

            # Check email uniqueness if being updated
            if update_data.email and update_data.email != user.email:
                if User.query.filter_by(email=update_data.email).first():
                    raise ValueError("Email already exists")
                user.email = update_data.email

            if update_data.full_name is not None:
                user.full_name = update_data.full_name

            if update_data.role is not None:
                user.role = update_data.role

            if update_data.is_active is not None:
                user.is_active = update_data.is_active

            db.session.commit()
            return user

        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email already exists")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to update user: {str(e)}")

    @staticmethod
    def change_password(user_id: int, password_data: ChangePasswordSchema) -> bool:
        """Change user password"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            if not user.check_password(password_data.current_password):
                raise ValueError("Current password is incorrect")

            user.set_password(password_data.new_password)
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to change password: {str(e)}")

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Delete a user (soft delete by deactivating)"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            user.is_active = False
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to delete user: {str(e)}")

    @staticmethod
    def generate_tokens(user: User):
        """Generate JWT tokens for user"""
        return JWTManager.generate_tokens(user)
