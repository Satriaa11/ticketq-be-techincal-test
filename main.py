from app import create_app


def main():
    """Main function to run the Flask application"""
    app = create_app()

    # Create database tables
    with app.app_context():
        from app.utils.extensions import db
        db.create_all()
        print("Database tables created successfully!")

    # Run the application
    print("Starting TicketQ API server...")
    print("API Documentation available at: http://127.0.0.1:5000/")
    print("Tickets endpoint: http://127.0.0.1:5000/tickets")

    app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    main()
