"""
Web routes for the Marathon Registration Application.
Provides HTML pages for viewing and managing events, participants, and invitations.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import MarathonEvent, Participant, Invitation
from app.validation import validate_event, validate_participant, validate_invitation
from datetime import datetime

# Create blueprint for web routes
web = Blueprint('web', __name__)


# ============================================================================
# Event Management Routes
# ============================================================================

@web.route('/')
@web.route('/events')
def events():
    """
    Display all marathon events with create/edit/delete functionality.
    Requirements: 1.2, 6.1
    """
    all_events = MarathonEvent.query.order_by(MarathonEvent.date.desc()).all()
    return render_template('events.html', events=all_events)


@web.route('/events/create', methods=['POST'])
def create_event_web():
    """
    Handle event creation from web form.
    Requirements: 1.1, 1.5, 6.1, 6.4, 6.5
    """
    data = {
        'name': request.form.get('name', '').strip(),
        'date': request.form.get('date', '').strip(),
        'location': request.form.get('location', '').strip(),
        'distance': request.form.get('distance', '').strip()
    }
    
    # Validate event data
    is_valid, errors = validate_event(data)
    
    if not is_valid:
        # Return validation errors as JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Flash errors for regular form submission
        for field, error in errors.items():
            flash(f'{field.capitalize()}: {error}', 'error')
        return redirect(url_for('web.events'))
    
    try:
        # Create new event
        new_event = MarathonEvent(
            name=data['name'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            location=data['location'],
            distance=float(data['distance'])
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        # Return success response for AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'event': {
                    'id': new_event.id,
                    'name': new_event.name,
                    'date': new_event.date.strftime('%Y-%m-%d'),
                    'location': new_event.location,
                    'distance': new_event.distance
                }
            }), 201
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('web.events'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while creating the event'}), 500
        
        flash('An error occurred while creating the event', 'error')
        return redirect(url_for('web.events'))


@web.route('/events/<int:id>/update', methods=['POST'])
def update_event_web(id):
    """
    Handle event update from web form.
    Requirements: 1.3, 1.5, 6.1, 6.4, 6.5
    """
    event = MarathonEvent.query.get(id)
    
    if not event:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        flash('Event not found', 'error')
        return redirect(url_for('web.events'))
    
    data = {
        'name': request.form.get('name', '').strip(),
        'date': request.form.get('date', '').strip(),
        'location': request.form.get('location', '').strip(),
        'distance': request.form.get('distance', '').strip()
    }
    
    # Validate event data
    is_valid, errors = validate_event(data)
    
    if not is_valid:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'errors': errors}), 400
        
        for field, error in errors.items():
            flash(f'{field.capitalize()}: {error}', 'error')
        return redirect(url_for('web.events'))
    
    try:
        # Update event
        event.name = data['name']
        event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        event.location = data['location']
        event.distance = float(data['distance'])
        
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'event': {
                    'id': event.id,
                    'name': event.name,
                    'date': event.date.strftime('%Y-%m-%d'),
                    'location': event.location,
                    'distance': event.distance
                }
            }), 200
        
        flash('Event updated successfully!', 'success')
        return redirect(url_for('web.events'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while updating the event'}), 500
        
        flash('An error occurred while updating the event', 'error')
        return redirect(url_for('web.events'))


@web.route('/events/<int:id>/delete', methods=['POST'])
def delete_event_web(id):
    """
    Handle event deletion from web form.
    Requirements: 1.4, 6.1, 6.4
    """
    event = MarathonEvent.query.get(id)
    
    if not event:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        flash('Event not found', 'error')
        return redirect(url_for('web.events'))
    
    try:
        db.session.delete(event)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True}), 200
        
        flash('Event deleted successfully!', 'success')
        return redirect(url_for('web.events'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while deleting the event'}), 500
        
        flash('An error occurred while deleting the event', 'error')
        return redirect(url_for('web.events'))


# ============================================================================
# Participant Management Routes
# ============================================================================

@web.route('/participants')
def participants():
    """
    Display all participants with create/edit/delete functionality.
    Requirements: 2.2, 6.2
    """
    all_participants = Participant.query.order_by(Participant.name).all()
    return render_template('participants.html', participants=all_participants)


@web.route('/participants/create', methods=['POST'])
def create_participant_web():
    """
    Handle participant creation from web form.
    Requirements: 2.1, 2.5, 6.2, 6.4, 6.5
    """
    data = {
        'name': request.form.get('name', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'age': request.form.get('age', '').strip()
    }
    
    # Validate participant data
    is_valid, errors = validate_participant(data)
    
    if not is_valid:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'errors': errors}), 400
        
        for field, error in errors.items():
            flash(f'{field.capitalize()}: {error}', 'error')
        return redirect(url_for('web.participants'))
    
    try:
        # Create new participant
        new_participant = Participant(
            name=data['name'],
            email=data['email'],
            phone=data['phone'] if data['phone'] else None,
            age=int(data['age'])
        )
        
        db.session.add(new_participant)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'participant': {
                    'id': new_participant.id,
                    'name': new_participant.name,
                    'email': new_participant.email,
                    'phone': new_participant.phone,
                    'age': new_participant.age
                }
            }), 201
        
        flash('Participant created successfully!', 'success')
        return redirect(url_for('web.participants'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while creating the participant'}), 500
        
        flash('An error occurred while creating the participant', 'error')
        return redirect(url_for('web.participants'))


@web.route('/participants/<int:id>/update', methods=['POST'])
def update_participant_web(id):
    """
    Handle participant update from web form.
    Requirements: 2.3, 2.5, 6.2, 6.4, 6.5
    """
    participant = Participant.query.get(id)
    
    if not participant:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Participant not found'}), 404
        flash('Participant not found', 'error')
        return redirect(url_for('web.participants'))
    
    data = {
        'name': request.form.get('name', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'age': request.form.get('age', '').strip()
    }
    
    # Validate participant data
    is_valid, errors = validate_participant(data)
    
    if not is_valid:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'errors': errors}), 400
        
        for field, error in errors.items():
            flash(f'{field.capitalize()}: {error}', 'error')
        return redirect(url_for('web.participants'))
    
    try:
        # Update participant
        participant.name = data['name']
        participant.email = data['email']
        participant.phone = data['phone'] if data['phone'] else None
        participant.age = int(data['age'])
        
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'participant': {
                    'id': participant.id,
                    'name': participant.name,
                    'email': participant.email,
                    'phone': participant.phone,
                    'age': participant.age
                }
            }), 200
        
        flash('Participant updated successfully!', 'success')
        return redirect(url_for('web.participants'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while updating the participant'}), 500
        
        flash('An error occurred while updating the participant', 'error')
        return redirect(url_for('web.participants'))


@web.route('/participants/<int:id>/delete', methods=['POST'])
def delete_participant_web(id):
    """
    Handle participant deletion from web form.
    Requirements: 2.4, 6.2, 6.4
    """
    participant = Participant.query.get(id)
    
    if not participant:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Participant not found'}), 404
        flash('Participant not found', 'error')
        return redirect(url_for('web.participants'))
    
    try:
        db.session.delete(participant)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True}), 200
        
        flash('Participant deleted successfully!', 'success')
        return redirect(url_for('web.participants'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while deleting the participant'}), 500
        
        flash('An error occurred while deleting the participant', 'error')
        return redirect(url_for('web.participants'))


# ============================================================================
# Invitation Management Routes
# ============================================================================

@web.route('/invitations')
def invitations():
    """
    Display all invitations with create/delete functionality.
    Requirements: 3.2, 6.3
    """
    all_invitations = Invitation.query.order_by(Invitation.sent_at.desc()).all()
    all_participants = Participant.query.order_by(Participant.name).all()
    all_events = MarathonEvent.query.order_by(MarathonEvent.date.desc()).all()
    
    return render_template(
        'invitations.html',
        invitations=all_invitations,
        participants=all_participants,
        events=all_events
    )


@web.route('/invitations/create', methods=['POST'])
def create_invitation_web():
    """
    Handle invitation creation from web form.
    Requirements: 3.1, 6.3, 6.4, 6.5
    """
    participant_id = request.form.get('participant_id', '').strip()
    event_id = request.form.get('event_id', '').strip()
    
    # Validate invitation data
    is_valid, errors = validate_invitation(participant_id, event_id)
    
    if not is_valid:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'errors': errors}), 400
        
        for field, error in errors.items():
            flash(f'{field.capitalize()}: {error}', 'error')
        return redirect(url_for('web.invitations'))
    
    try:
        # Create new invitation
        new_invitation = Invitation(
            participant_id=int(participant_id),
            event_id=int(event_id)
        )
        
        db.session.add(new_invitation)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'invitation': {
                    'id': new_invitation.id,
                    'participant': {
                        'id': new_invitation.participant.id,
                        'name': new_invitation.participant.name,
                        'email': new_invitation.participant.email
                    },
                    'event': {
                        'id': new_invitation.event.id,
                        'name': new_invitation.event.name,
                        'date': new_invitation.event.date.strftime('%Y-%m-%d'),
                        'location': new_invitation.event.location
                    },
                    'sent_at': new_invitation.sent_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }), 201
        
        flash('Invitation created successfully!', 'success')
        return redirect(url_for('web.invitations'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while creating the invitation'}), 500
        
        flash('An error occurred while creating the invitation', 'error')
        return redirect(url_for('web.invitations'))


@web.route('/invitations/<int:id>/delete', methods=['POST'])
def delete_invitation_web(id):
    """
    Handle invitation deletion from web form.
    Requirements: 3.5, 6.3, 6.4
    """
    invitation = Invitation.query.get(id)
    
    if not invitation:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Invitation not found'}), 404
        flash('Invitation not found', 'error')
        return redirect(url_for('web.invitations'))
    
    try:
        db.session.delete(invitation)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True}), 200
        
        flash('Invitation deleted successfully!', 'success')
        return redirect(url_for('web.invitations'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'An error occurred while deleting the invitation'}), 500
        
        flash('An error occurred while deleting the invitation', 'error')
        return redirect(url_for('web.invitations'))
