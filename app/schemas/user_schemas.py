from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from enum import Enum


class UserRole(str, Enum):
    """User roles enum"""
    ADMIN = "admin"
    USER = "user"


class UserCreateSchema(BaseModel):
    """Schema for creating a new user"""
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username for the user"
    )
    email: EmailStr = Field(
        ...,
        description="Email address"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)"
    )
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Full name of the user"
    )
    role: UserRole = Field(
        default=UserRole.USER,
        description="User role (admin or user)"
    )

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        return v.lower()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLoginSchema(BaseModel):
    """Schema for user login"""
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponseSchema(BaseModel):
    """Schema for user response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    """Schema for updating user"""
    model_config = ConfigDict(str_strip_whitespace=True)

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class TokenResponseSchema(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponseSchema


class RefreshTokenSchema(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str = Field(..., description="Refresh token")


class ChangePasswordSchema(BaseModel):
    """Schema for changing password"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
