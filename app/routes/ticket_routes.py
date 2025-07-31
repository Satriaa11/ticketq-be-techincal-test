from flask import Blueprint
from app.controllers.ticket_controller import TicketController

# Create tickets blueprint
tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')

# Define routes
tickets_bp.route('/', methods=['GET'])(TicketController.get_all_tickets)
tickets_bp.route('/', methods=['POST'])(TicketController.create_ticket)
tickets_bp.route('/<int:ticket_id>', methods=['GET'])(TicketController.get_ticket_by_id)
tickets_bp.route('/<int:ticket_id>', methods=['PATCH'])(TicketController.update_ticket_status)
tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])(TicketController.delete_ticket)
