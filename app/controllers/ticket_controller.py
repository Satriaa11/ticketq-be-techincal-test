from flask import request, jsonify
from pydantic import ValidationError
from app.services.ticket_service import TicketService
from app.utils.auth import token_required, admin_required, optional_auth
from app.schemas.ticket_schemas import (
    TicketCreateSchema,
    TicketUpdateSchema,
    TicketResponseSchema,
    TicketListResponseSchema,
    ErrorResponseSchema
)
import math


class TicketController:
    """Controller for ticket endpoints"""

    @staticmethod
    @token_required
    def create_ticket(current_user):
        """POST /tickets - Create a new ticket (Authentication required)"""
        try:
            # Validate request data
            ticket_data = TicketCreateSchema(**request.get_json())

            # Create ticket with user info
            new_ticket = TicketService.create_ticket(ticket_data, current_user.id)

            # Return response
            response_data = TicketResponseSchema.model_validate(new_ticket)
            return jsonify(response_data.model_dump()), 201

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
    @optional_auth
    def get_all_tickets(current_user):
        """GET /tickets - List all tickets (Optional authentication)"""
        try:
            # Get pagination parameters
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 per page

            # Get tickets based on user role
            if current_user and current_user.is_admin():
                # Admin can see all tickets
                tickets, total = TicketService.get_all_tickets(page, per_page)
            elif current_user:
                # Regular users can see all tickets but with limited info
                tickets, total = TicketService.get_all_tickets(page, per_page)
            else:
                # Anonymous users can see all tickets but with limited info
                tickets, total = TicketService.get_all_tickets(page, per_page)

            # Calculate total pages
            total_pages = math.ceil(total / per_page)

            # Convert to response schema
            ticket_responses = [TicketResponseSchema.model_validate(ticket) for ticket in tickets]

            response_data = TicketListResponseSchema(
                tickets=ticket_responses,
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages
            )

            return jsonify(response_data.model_dump()), 200

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500

    @staticmethod
    @optional_auth
    def get_ticket_by_id(current_user, ticket_id):
        """GET /tickets/:id - View a specific ticket (Optional authentication)"""
        try:
            ticket = TicketService.get_ticket_by_id(ticket_id)

            if not ticket:
                error_response = ErrorResponseSchema(
                    error="Not Found",
                    message=f"Ticket with ID {ticket_id} not found",
                    status_code=404
                )
                return jsonify(error_response.model_dump()), 404

            response_data = TicketResponseSchema.model_validate(ticket)
            return jsonify(response_data.model_dump()), 200

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500

    @staticmethod
    @token_required
    def update_ticket_status(current_user, ticket_id):
        """PATCH /tickets/:id - Mark a ticket as used (Authentication required)"""
        try:
            # Validate request data
            update_data = TicketUpdateSchema(**request.get_json())

            # Check permission: user can only update their own tickets, admin can update any
            ticket = TicketService.get_ticket_by_id(ticket_id)
            if not ticket:
                error_response = ErrorResponseSchema(
                    error="Not Found",
                    message=f"Ticket with ID {ticket_id} not found",
                    status_code=404
                )
                return jsonify(error_response.model_dump()), 404

            # Permission check
            if not current_user.is_admin() and ticket.created_by_id != current_user.id:
                error_response = ErrorResponseSchema(
                    error="Forbidden",
                    message="You can only update your own tickets",
                    status_code=403
                )
                return jsonify(error_response.model_dump()), 403

            # Update ticket
            updated_ticket = TicketService.update_ticket_status(ticket_id, update_data)

            response_data = TicketResponseSchema.model_validate(updated_ticket)
            return jsonify(response_data.model_dump()), 200

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
    def delete_ticket(current_user, ticket_id):
        """DELETE /tickets/:id - Remove a ticket (Admin only)"""
        try:
            deleted = TicketService.delete_ticket(ticket_id)

            if not deleted:
                error_response = ErrorResponseSchema(
                    error="Not Found",
                    message=f"Ticket with ID {ticket_id} not found",
                    status_code=404
                )
                return jsonify(error_response.model_dump()), 404

            return jsonify({"message": f"Ticket {ticket_id} deleted successfully"}), 200

        except Exception as e:
            error_response = ErrorResponseSchema(
                error="Internal Server Error",
                message=str(e),
                status_code=500
            )
            return jsonify(error_response.model_dump()), 500
