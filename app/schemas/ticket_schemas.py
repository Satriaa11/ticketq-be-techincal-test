from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class TicketCreateSchema(BaseModel):
    """Schema for creating a new ticket"""
    model_config = ConfigDict(str_strip_whitespace=True)

    event_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the event"
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Location of the event"
    )
    time: datetime = Field(
        ...,
        description="Event time in ISO format"
    )

    @field_validator('event_name')
    @classmethod
    def validate_event_name(cls, v):
        if not v or v.isspace():
            raise ValueError('Event name is required and cannot be empty')
        return v.strip()

    @field_validator('location')
    @classmethod
    def validate_location(cls, v):
        if not v or v.isspace():
            raise ValueError('Location is required and cannot be empty')
        return v.strip()

    @field_validator('time')
    @classmethod
    def validate_time(cls, v):
        if v < datetime.now():
            raise ValueError('Event time cannot be in the past')
        return v


class TicketUpdateSchema(BaseModel):
    """Schema for updating ticket status (mark as used)"""
    model_config = ConfigDict(str_strip_whitespace=True)

    is_used: bool = Field(
        ...,
        description="Mark ticket as used or unused"
    )


class TicketResponseSchema(BaseModel):
    """Schema for ticket response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_name: str
    location: str
    time: datetime
    is_used: bool
    created_at: datetime
    updated_at: datetime


class TicketListResponseSchema(BaseModel):
    """Schema for list of tickets response"""
    tickets: list[TicketResponseSchema]
    total: int
    page: int
    per_page: int
    total_pages: int


class ErrorResponseSchema(BaseModel):
    """Schema for error responses"""
    error: str
    message: str
    status_code: int
    details: Optional[dict] = None
