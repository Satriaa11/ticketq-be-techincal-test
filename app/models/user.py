from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.extensions import db
from app.schemas.user_schemas import UserRole


class User(db.Model):
    """User model for database"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship dengan tickets (user yang membuat ticket)
    tickets = db.relationship('Ticket', backref='created_by', lazy=True, foreign_keys='Ticket.created_by_id')

    def __repr__(self):
        return f'<User {self.username}: {self.role}>'

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user is admin"""
        return self.role == UserRole.ADMIN

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
