from flask import request, jsonify
from pydantic import ValidationError
from app.services.ticket_service import TicketService
from app.schemas.ticket_schemas import TicketCreateSchema, TicketUpdateSchema


class TicketController:
    """Controller for ticket operations - Pure business logic"""

    @staticmethod
    def get_all_tickets():
        """Get all tickets with pagination"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            tickets_pagination = TicketService.get_all_tickets(page=page, per_page=per_page)

            return jsonify({
                'tickets': [ticket.to_dict() for ticket in tickets_pagination.items],
                'pagination': {
                    'page': tickets_pagination.page,
                    'pages': tickets_pagination.pages,
                    'per_page': tickets_pagination.per_page,
                    'total': tickets_pagination.total,
                    'has_next': tickets_pagination.has_next,
                    'has_prev': tickets_pagination.has_prev
                }
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500

    @staticmethod
    def get_ticket_by_id(ticket_id):
        """Get a specific ticket by ID"""
        try:
            ticket = TicketService.get_ticket_by_id(ticket_id)
            if not ticket:
                return jsonify({
                    'error': 'Not Found',
                    'message': 'Ticket not found'
                }), 404

            return jsonify(ticket.to_dict()), 200

        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500

    @staticmethod
    def create_ticket():
        """Create a new ticket"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': 'No JSON data provided'
                }), 400

            # Validate input using Pydantic
            ticket_data = TicketCreateSchema(**data)

            # Create ticket
            ticket = TicketService.create_ticket(ticket_data.model_dump())

            return jsonify({
                'message': 'Ticket created successfully',
                'ticket': ticket.to_dict()
            }), 201

        except ValidationError as e:
            # Convert Pydantic errors to JSON-serializable format
            error_details = []
            for error in e.errors():
                error_details.append({
                    'field': error.get('loc', ['unknown'])[0] if error.get('loc') else 'unknown',
                    'message': error.get('msg', 'Validation error'),
                    'type': error.get('type', 'validation_error'),
                    'input': str(error.get('input', ''))
                })

            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input data',
                'details': error_details
            }), 400

        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500

    @staticmethod
    def update_ticket(ticket_id):
        """Update ticket (mark as used/unused)"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': 'No JSON data provided'
                }), 400

            # Validate input using Pydantic
            update_data = TicketUpdateSchema(**data)

            # Update ticket
            ticket = TicketService.mark_ticket_as_used(ticket_id, update_data.isUsed)
            if not ticket:
                return jsonify({
                    'error': 'Not Found',
                    'message': 'Ticket not found'
                }), 404

            return jsonify({
                'message': 'Ticket updated successfully',
                'ticket': ticket.to_dict()
            }), 200

        except ValidationError as e:
            # Convert Pydantic errors to JSON-serializable format
            error_details = []
            for error in e.errors():
                error_details.append({
                    'field': error.get('loc', ['unknown'])[0] if error.get('loc') else 'unknown',
                    'message': error.get('msg', 'Validation error'),
                    'type': error.get('type', 'validation_error'),
                    'input': str(error.get('input', ''))
                })

            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input data',
                'details': error_details
            }), 400

        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500

    @staticmethod
    def delete_ticket(ticket_id):
        """Delete a ticket"""
        try:
            success = TicketService.delete_ticket(ticket_id)
            if not success:
                return jsonify({
                    'error': 'Not Found',
                    'message': 'Ticket not found'
                }), 404

            return jsonify({
                'message': 'Ticket deleted successfully'
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e)
            }), 500
