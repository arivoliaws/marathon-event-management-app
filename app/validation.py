"""
Validation module for Marathon Registration Application.

This module provides validation functions for events, participants, and invitations.
Each validation function returns a tuple of (is_valid: bool, errors: dict).
"""

import re
from datetime import date
from app.models import Participant, MarathonEvent


def validate_event(data):
    """
    Validate marathon event data.
    
    Checks:
    - name is non-empty
    - date is a valid future date
    - location is non-empty
    - distance is a positive number
    
    Args:
        data: Dictionary containing event fields (name, date, location, distance)
        
    Returns:
        Tuple of (is_valid: bool, errors: dict)
        errors dict contains field-specific error messages
    """
    errors = {}
    
    # Validate name
    name = data.get('name', '').strip()
    if not name:
        errors['name'] = 'Name is required and cannot be empty'
    
    # Validate date
    event_date = data.get('date')
    if not event_date:
        errors['date'] = 'Date is required'
    else:
        # Handle both date objects and string dates
        if isinstance(event_date, str):
            try:
                from datetime import datetime
                event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
            except ValueError:
                errors['date'] = 'Date must be in YYYY-MM-DD format'
                event_date = None
        
        # Check if date is in the future
        if event_date and event_date <= date.today():
            errors['date'] = 'Date must be in the future'
    
    # Validate location
    location = data.get('location', '').strip()
    if not location:
        errors['location'] = 'Location is required and cannot be empty'
    
    # Validate distance
    distance = data.get('distance')
    if distance is None:
        errors['distance'] = 'Distance is required'
    else:
        try:
            distance_float = float(distance)
            if distance_float <= 0:
                errors['distance'] = 'Distance must be a positive number'
        except (ValueError, TypeError):
            errors['distance'] = 'Distance must be a valid number'
    
    is_valid = len(errors) == 0
    return (is_valid, errors)


def validate_participant(data):
    """
    Validate participant data.
    
    Checks:
    - name is non-empty
    - email follows valid email format
    - age is a positive integer
    
    Args:
        data: Dictionary containing participant fields (name, email, age)
        
    Returns:
        Tuple of (is_valid: bool, errors: dict)
        errors dict contains field-specific error messages
    """
    errors = {}
    
    # Validate name
    name = data.get('name', '').strip()
    if not name:
        errors['name'] = 'Name is required and cannot be empty'
    
    # Validate email
    email = data.get('email', '').strip()
    if not email:
        errors['email'] = 'Email is required'
    else:
        # Basic email format validation using regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors['email'] = 'Email must be in valid format (e.g., user@example.com)'
    
    # Validate age
    age = data.get('age')
    if age is None:
        errors['age'] = 'Age is required'
    else:
        try:
            age_int = int(age)
            if age_int <= 0:
                errors['age'] = 'Age must be a positive integer'
        except (ValueError, TypeError):
            errors['age'] = 'Age must be a valid integer'
    
    is_valid = len(errors) == 0
    return (is_valid, errors)


def validate_invitation(participant_id, event_id):
    """
    Validate invitation data by checking referential integrity.
    
    Checks:
    - participant exists in the database
    - event exists in the database
    
    Args:
        participant_id: ID of the participant
        event_id: ID of the marathon event
        
    Returns:
        Tuple of (is_valid: bool, errors: dict)
        errors dict contains field-specific error messages
    """
    from app import db
    errors = {}
    
    # Check if participant_id is provided
    if participant_id is None:
        errors['participant_id'] = 'Participant ID is required'
    else:
        # Check if participant exists (using SQLAlchemy 2.0 syntax)
        participant = db.session.get(Participant, participant_id)
        if not participant:
            errors['participant_id'] = 'Participant not found'
    
    # Check if event_id is provided
    if event_id is None:
        errors['event_id'] = 'Event ID is required'
    else:
        # Check if event exists (using SQLAlchemy 2.0 syntax)
        event = db.session.get(MarathonEvent, event_id)
        if not event:
            errors['event_id'] = 'Event not found'
    
    is_valid = len(errors) == 0
    return (is_valid, errors)
