from flask import Blueprint
from flasgger import swag_from
from app.controllers.ticket_controller import TicketController

# Create blueprint
tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')


@tickets_bp.route('', methods=['GET'])
@swag_from('../docs/swagger/tickets/get_tickets.yml')
def get_tickets():
    """Get all tickets endpoint"""
    return TicketController.get_all_tickets()


@tickets_bp.route('', methods=['POST'])
@swag_from('../docs/swagger/tickets/create_ticket.yml')
def create_ticket():
    """Create ticket endpoint"""
    return TicketController.create_ticket()


@tickets_bp.route('/<int:ticket_id>', methods=['GET'])
@swag_from('../docs/swagger/tickets/get_ticket.yml')
def get_ticket(ticket_id):
    """Get single ticket endpoint"""
    return TicketController.get_ticket_by_id(ticket_id)


@tickets_bp.route('/<int:ticket_id>', methods=['PATCH'])
@swag_from('../docs/swagger/tickets/update_ticket.yml')
def update_ticket(ticket_id):
    """Update ticket endpoint"""
    return TicketController.update_ticket(ticket_id)


@tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])
@swag_from('../docs/swagger/tickets/delete_ticket.yml')
def delete_ticket(ticket_id):
    """Delete ticket endpoint"""
    return TicketController.delete_ticket(ticket_id)
