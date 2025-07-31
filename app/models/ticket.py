from datetime import datetime
from app.utils.extensions import db


class Ticket(db.Model):
    """Ticket model for database"""
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Ticket {self.id}: {self.event_name}>'

    def to_dict(self):
        """Convert ticket to dictionary"""
        return {
            'id': self.id,
            'event_name': self.event_name,
            'location': self.location,
            'time': self.time,
            'is_used': self.is_used,
            'created_by_id': self.created_by_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
