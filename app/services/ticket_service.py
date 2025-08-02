from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.models.ticket import Ticket
from app.utils.extensions import db


class TicketService:
    """Service class for ticket business logic"""

    @staticmethod
    def get_all_tickets(page: int = 1, per_page: int = 10):
        """Get all tickets with pagination"""
        try:
            return Ticket.query.order_by(Ticket.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def get_ticket_by_id(ticket_id: int) -> Optional[Ticket]:
        """Get a ticket by ID"""
        try:
            return Ticket.query.get(ticket_id)
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def create_ticket(ticket_data: Dict[str, Any]) -> Ticket:
        """Create a new ticket"""
        try:
            ticket = Ticket(
                event_name=ticket_data['eventName'],
                location=ticket_data['location'],
                time=ticket_data['time']
            )
            db.session.add(ticket)
            db.session.commit()
            return ticket
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to create ticket: {str(e)}")

    @staticmethod
    def mark_ticket_as_used(ticket_id: int, is_used: bool) -> Optional[Ticket]:
        """Mark a ticket as used or unused"""
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return None

            ticket.is_used = is_used
            db.session.commit()
            return ticket
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to update ticket: {str(e)}")

    @staticmethod
    def delete_ticket(ticket_id: int) -> bool:
        """Delete a ticket"""
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return False

            db.session.delete(ticket)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to delete ticket: {str(e)}")
