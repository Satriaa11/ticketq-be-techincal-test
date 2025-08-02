from datetime import datetime
from app.utils.extensions import db


class Ticket(db.Model):
    """Ticket model for event tickets"""
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Ticket {self.id}: {self.event_name}>'

    def to_dict(self):
        """Convert ticket to dictionary"""
        return {
            'id': self.id,
            'eventName': self.event_name,
            'location': self.location,
            'time': self.time.isoformat() if self.time else None,
            'isUsed': self.is_used,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
