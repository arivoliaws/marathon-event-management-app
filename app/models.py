from datetime import datetime
from app import db


class MarathonEvent(db.Model):
    __tablename__ = 'marathon_events'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to invitations
    invitations = db.relationship('Invitation', back_populates='event', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'distance': self.distance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to invitations
    invitations = db.relationship('Invitation', back_populates='participant', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Invitation(db.Model):
    __tablename__ = 'invitations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('marathon_events.id', ondelete='CASCADE'), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    participant = db.relationship('Participant', back_populates='invitations')
    event = db.relationship('MarathonEvent', back_populates='invitations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'event_id': self.event_id,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'participant': self.participant.to_dict() if self.participant else None,
            'event': self.event.to_dict() if self.event else None
        }
