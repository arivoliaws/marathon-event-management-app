"""
REST API Blueprint for Marathon Registration Application.

This module provides REST API endpoints for CRUD operations on events, participants, and invitations.
All endpoints return JSON responses with appropriate HTTP status codes.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import MarathonEvent, Participant, Invitation
from app.validation import validate_event, validate_participant, validate_invitation

api = Blueprint('api', __name__, url_prefix='/api')


# ============================================================================
# Marathon Events API Endpoints
# ============================================================================

@api.route('/events', methods=['POST'])
def create_event():
    """
    Create a new marathon event.
    
    Request Body (JSON):
        - name: string (required)
        - date: string in YYYY-MM-DD format (required)
        - location: string (required)
        - distance: number (required, positive)
    
    Returns:
        201: Event created successfully with event JSON
        400: Validation failed with error details
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate event data
        is_valid, errors = validate_event(data)
        if not is_valid:
            return jsonify({
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        # Create new event
        event = MarathonEvent(
            name=data['name'].strip(),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            location=data['location'].strip(),
            distance=float(data['distance'])
        )
        
        # Persist to database
        db.session.add(event)
        db.session.commit()
        
        return jsonify(event.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/events', methods=['GET'])
def get_events():
    """
    Get all marathon events.
    
    Returns:
        200: List of all events as JSON array
        500: Server error
    """
    try:
        events = MarathonEvent.query.all()
        return jsonify([event.to_dict() for event in events]), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    """
    Get a specific marathon event by ID.
    
    Args:
        id: Event ID
    
    Returns:
        200: Event JSON
        404: Event not found
        500: Server error
    """
    try:
        event = db.session.get(MarathonEvent, id)
        
        if not event:
            return jsonify({
                'error': 'Resource not found',
                'resource_type': 'event',
                'id': id
            }), 404
        
        return jsonify(event.to_dict()), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    """
    Update an existing marathon event.
    
    Args:
        id: Event ID
    
    Request Body (JSON):
        - name: string (optional)
        - date: string in YYYY-MM-DD format (optional)
        - location: string (optional)
        - distance: number (optional, positive)
    
    Returns:
        200: Event updated successfully with event JSON
        400: Validation failed with error details
        404: Event not found
        500: Server error
    """
    try:
        event = db.session.get(MarathonEvent, id)
        
        if not event:
            return jsonify({
                'error': 'Resource not found',
                'resource_type': 'event',
                'id': id
            }), 404
        
        data = request.get_json()
        
        # Merge existing data with update data for validation
        update_data = {
            'name': data.get('name', event.name),
            'date': data.get('date', event.date),
            'location': data.get('location', event.location),
            'distance': data.get('distance', event.distance)
        }
        
        # Validate updated data
        is_valid, errors = validate_event(update_data)
        if not is_valid:
            return jsonify({
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        # Update event fields
        if 'name' in data:
            event.name = data['name'].strip()
        if 'date' in data:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'location' in data:
            event.location = data['location'].strip()
        if 'distance' in data:
            event.distance = float(data['distance'])
        
        # Update timestamp
        event.updated_at = datetime.utcnow()
        
        # Persist changes
        db.session.commit()
        
        return jsonify(event.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    """
    Delete a marathon event.
    
    Args:
        id: Event ID
    
    Returns:
        204: Event deleted successfully (no content)
        404: Event not found
        500: Server error
    """
    try:
        event = db.session.get(MarathonEvent, id)
        
        if not event:
            return jsonify({
                'error': 'Resource not found',
                'resource_type': 'event',
                'id': id
            }), 404
        
        # Delete event (cascade will handle invitations)
        db.session.delete(event)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


# ============================================================================
# Participants API Endpoints
# ============================================================================

@api.route('/participants', methods=['POST'])
def create_participant():
    """
    Create a new participant.
    
    Request Body (JSON):
        - name: string (required)
        - email: string (required, valid email format)
        - phone: string (optional)
        - age: integer (required, positive)
    
    Returns:
        201: Participant created successfully with participant JSON
        400: Validation failed with error details
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate participant data
        is_valid, errors = validate_participant(data)
        if not is_valid:
            return jsonify({
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        # Create new participant
        participant = Participant(
            name=data['name'].strip(),
            email=data['email'].strip(),
            phone=data.get('phone', '').strip() if data.get('phone') else None,
            age=int(data['age'])
        )
        
        # Persist to database
        db.session.add(participant)
        db.session.commit()
        
        return jsonify(participant.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/participants', methods=['GET'])
def get_participants():
    """
    Get all participants.
    
    Returns:
        200: List of all participants as JSON array
        500: Server error
    """
    try:
        participants = Participant.query.all()
        return jsonify([participant.to_dict() for participant in participants]), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/participants/<int:id>', methods=['GET'])
def get_participant(id):
    """
    Get a specific participant by ID.
    
    Args:
        id: Participant ID
    
    Returns:
        200: Participant JSON
        404: Participant not found
        500: Server error
    """
    try:
        participant = db.session.get(Participant, id)
        
        if not participant:
            return jsonify({
                'error': 'Resource not found',
                'resource_type': 'participant',
                'id': id
            }), 404
        
        return jsonify(participant.to_dict()), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/participants/<int:id>', methods=['PUT'])
def update_participant(id):
    """
    Update an existing participant.
    
    Args:
        id: Participant ID
    
    Request Body (JSON):
        - name: string (optional)
        - email: string (optional, valid email format)
        - phone: string (optional)
        - age: integer (optional, positive)
    
    Returns:
        200: Participant updated successfully with participant JSON
        400: Validation failed with error details
        404: Participant not found
        500: Server error
    """
    try:
        participant = db.session.get(Participant, id)
        
        if not participant:
            return jsonify({
                'error': 'Resource not found',
                'resource_type': 'participant',
                'id': id
            }), 404
        
        data = request.get_json()
        
        # Merge existing data with update data for validation
        update_data = {
            'name': data.get('name', participant.name),
            'email': data.get('email', participant.email),
            'age': data.get('age', participant.age)
        }
        
        # Validate updated data
        is_valid, errors = validate_participant(update_data)
        if not is_valid:
            return jsonify({
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        # Update participant fields
        if 'name' in data:
            participant.name = data['name'].strip()
        if 'email' in data:
            participant.email = data['email'].strip()
        if 'phone' in data:
            participant.phone = data['phone'].strip() if data['phone'] else None
        if 'age' in data:
            participant.age = int(data['age'])
        
        # Update timestamp
        participant.updated_at = datetime.utcnow()
        
        # Persist changes
        db.session.commit()
        
        return jsonify(participant.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/participants/<int:id>', methods=['DELETE'])
def delete_participant(id):
    """
    Delete a participant.
    
    Args:
        id: Participant ID
    
    Returns:
        204: Participant deleted successfully (no content)
        404: Participant not found
        500: Server error
    """
    try:
        participant = db.session.get(Participant, id)
        
        if not participant:
            return jsonify({
                'error': 'Resource not found',
                'resource_type': 'participant',
                'id': id
            }), 404
        
        # Delete participant (cascade will handle invitations)
        db.session.delete(participant)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


# ============================================================================
# Invitations API Endpoints
# ============================================================================

@api.route('/invitations', methods=['POST'])
def create_invitation():
    """
    Create a new invitation.
    
    Request Body (JSON):
        - participant_id: integer (required)
        - event_id: integer (required)
    
    Returns:
        201: Invitation created successfully with invitation JSON (includes nested participant/event data)
        400: Validation failed with error details
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Extract participant_id and event_id
        participant_id = data.get('participant_id')
        event_id = data.get('event_id')
        
        # Validate invitation data (checks referential integrity)
        is_valid, errors = validate_invitation(participant_id, event_id)
        if not is_valid:
            return jsonify({
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        # Create new invitation
        invitation = Invitation(
            participant_id=participant_id,
            event_id=event_id
        )
        
        # Persist to database
        db.session.add(invitation)
        db.session.commit()
        
        return jsonify(invitation.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/invitations', methods=['GET'])
def get_invitations():
    """
    Get all invitations or filter by event_id or participant_id.
    
    Query Parameters:
        - event_id: integer (optional) - filter invitations by event
        - participant_id: integer (optional) - filter invitations by participant
    
    Returns:
        200: List of invitations as JSON array (includes nested participant/event data)
        500: Server error
    """
    try:
        # Get query parameters
        event_id = request.args.get('event_id', type=int)
        participant_id = request.args.get('participant_id', type=int)
        
        # Build query based on filters
        query = Invitation.query
        
        if event_id is not None:
            query = query.filter_by(event_id=event_id)
        
        if participant_id is not None:
            query = query.filter_by(participant_id=participant_id)
        
        # Execute query
        invitations = query.all()
        
        return jsonify([invitation.to_dict() for invitation in invitations]), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500


@api.route('/invitations/<int:id>', methods=['DELETE'])
def delete_invitation(id):
    """
    Delete an invitation.
    
    Args:
        id: Invitation ID
    
    Returns:
        204: Invitation deleted successfully (no content)
        404: Invitation not found
        500: Server error
    """
    try:
        invitation = db.session.get(Invitation, id)
        
        if not invitation:
            return jsonify({
                'error': 'Resource not found',
                'resource_type': 'invitation',
                'id': id
            }), 404
        
        # Delete invitation
        db.session.delete(invitation)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500
