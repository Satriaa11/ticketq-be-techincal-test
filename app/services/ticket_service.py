from typing import Optional, List, Tuple
from sqlalchemy.exc import SQLAlchemyError
from app.models.ticket import Ticket
from app.utils.extensions import db
from app.schemas.ticket_schemas import TicketCreateSchema, TicketUpdateSchema


class TicketService:
    """Service layer for ticket operations"""

    @staticmethod
    def create_ticket(ticket_data: TicketCreateSchema, created_by_id: int = None) -> Ticket:
        """Create a new ticket"""
        try:
            new_ticket = Ticket(
                event_name=ticket_data.event_name,
                location=ticket_data.location,
                time=ticket_data.time,
                created_by_id=created_by_id
            )

            db.session.add(new_ticket)
            db.session.commit()
            return new_ticket

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to create ticket: {str(e)}")

    @staticmethod
    def get_ticket_by_id(ticket_id: int) -> Optional[Ticket]:
        """Get a ticket by ID"""
        try:
            return Ticket.query.get(ticket_id)
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve ticket: {str(e)}")

    @staticmethod
    def get_all_tickets(page: int = 1, per_page: int = 10) -> Tuple[List[Ticket], int]:
        """Get all tickets with pagination"""
        try:
            pagination = Ticket.query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            return pagination.items, pagination.total
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve tickets: {str(e)}")

    @staticmethod
    def update_ticket_status(ticket_id: int, update_data: TicketUpdateSchema) -> Optional[Ticket]:
        """Update ticket status (mark as used/unused)"""
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return None

            ticket.is_used = update_data.is_used
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
