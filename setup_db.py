#!/usr/bin/env python3
"""Database migration and admin setup script"""

from app import create_app
from app.utils.extensions import db
from app.models import User, Ticket
from app.schemas.user_schemas import UserRole
import sys


def setup_database():
    """Initialize database and create admin user"""
    app = create_app()

    with app.app_context():
        try:
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created successfully!")

            # Check if admin user already exists
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                print("✓ Admin user already exists!")
                print(f"  Username: {admin_user.username}")
                print(f"  Email: {admin_user.email}")
                return

            # Create admin user
            print("Creating default admin user...")
            admin_user = User(
                username='admin',
                email='admin@ticketq.com',
                full_name='System Administrator',
                role=UserRole.ADMIN
            )
            admin_user.set_password('Admin123!')

            db.session.add(admin_user)
            db.session.commit()

            print("✓ Admin user created successfully!")
            print("  Username: admin")
            print("  Email: admin@ticketq.com")
            print("  Password: Admin123!")
            print("  Role: admin")
            print("")
            print("⚠️  Please change the default admin password after first login!")

        except Exception as e:
            print(f"❌ Error setting up database: {str(e)}")
            sys.exit(1)


def reset_database():
    """Reset database (drop and recreate all tables)"""
    app = create_app()

    with app.app_context():
        try:
            print("⚠️  Dropping all database tables...")
            db.drop_all()
            print("✓ All tables dropped!")

            print("Creating new database tables...")
            db.create_all()
            print("✓ Database tables recreated!")

            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@ticketq.com',
                full_name='System Administrator',
                role=UserRole.ADMIN
            )
            admin_user.set_password('Admin123!')

            db.session.add(admin_user)
            db.session.commit()

            print("✓ Default admin user created!")
            print("  Username: admin")
            print("  Password: Admin123!")

        except Exception as e:
            print(f"❌ Error resetting database: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        setup_database()
