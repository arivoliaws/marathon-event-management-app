"""
Unit tests for Invitation API endpoints.

Tests cover CRUD operations, validation, error handling, HTTP status codes,
and filtering by event_id and participant_id.
"""

import pytest
import json
from datetime import date, timedelta
from app import create_app, db
from app.models import MarathonEvent, Participant, Invitation


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_event(app):
    """Create a sample event in the database."""
    with app.app_context():
        event = MarathonEvent(
            name='Test Marathon',
            date=date.today() + timedelta(days=30),
            location='Test Location',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    return event_id


@pytest.fixture
def sample_participant(app):
    """Create a sample participant in the database."""
    with app.app_context():
        participant = Participant(
            name='John Doe',
            email='john@example.com',
            phone='555-1234',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    return participant_id


@pytest.fixture
def multiple_events(app):
    """Create multiple events in the database."""
    with app.app_context():
        event1 = MarathonEvent(
            name='Marathon 1',
            date=date.today() + timedelta(days=30),
            location='Location 1',
            distance=42.195
        )
        event2 = MarathonEvent(
            name='Marathon 2',
            date=date.today() + timedelta(days=60),
            location='Location 2',
            distance=21.0975
        )
        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()
        event_ids = [event1.id, event2.id]
    return event_ids


@pytest.fixture
def multiple_participants(app):
    """Create multiple participants in the database."""
    with app.app_context():
        participant1 = Participant(
            name='John Doe',
            email='john@example.com',
            age=30
        )
        participant2 = Participant(
            name='Jane Smith',
            email='jane@example.com',
            age=25
        )
        db.session.add(participant1)
        db.session.add(participant2)
        db.session.commit()
        participant_ids = [participant1.id, participant2.id]
    return participant_ids


# ============================================================================
# POST /api/invitations - Create Invitation Tests
# ============================================================================

def test_create_invitation_success(client, sample_event, sample_participant):
    """Test creating a valid invitation returns 201 with invitation data."""
    invitation_data = {
        'participant_id': sample_participant,
        'event_id': sample_event
    }
    
    response = client.post('/api/invitations',
                          data=json.dumps(invitation_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['participant_id'] == sample_participant
    assert data['event_id'] == sample_event
    assert 'id' in data
    assert 'sent_at' in data
    # Verify nested participant and event data
    assert 'participant' in data
    assert data['participant']['id'] == sample_participant
    assert data['participant']['name'] == 'John Doe'
    assert 'event' in data
    assert data['event']['id'] == sample_event
    assert data['event']['name'] == 'Test Marathon'


def test_create_invitation_nonexistent_participant(client, sample_event):
    """Test creating invitation with non-existent participant returns 400."""
    invitation_data = {
        'participant_id': 999,
        'event_id': sample_event
    }
    
    response = client.post('/api/invitations',
                          data=json.dumps(invitation_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data
    assert 'participant_id' in data['details']
    assert 'not found' in data['details']['participant_id'].lower()


def test_create_invitation_nonexistent_event(client, sample_participant):
    """Test creating invitation with non-existent event returns 400."""
    invitation_data = {
        'participant_id': sample_participant,
        'event_id': 999
    }
    
    response = client.post('/api/invitations',
                          data=json.dumps(invitation_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data
    assert 'event_id' in data['details']
    assert 'not found' in data['details']['event_id'].lower()


def test_create_invitation_missing_participant_id(client, sample_event):
    """Test creating invitation without participant_id returns 400."""
    invitation_data = {
        'event_id': sample_event
    }
    
    response = client.post('/api/invitations',
                          data=json.dumps(invitation_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'participant_id' in data['details']


def test_create_invitation_missing_event_id(client, sample_participant):
    """Test creating invitation without event_id returns 400."""
    invitation_data = {
        'participant_id': sample_participant
    }
    
    response = client.post('/api/invitations',
                          data=json.dumps(invitation_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'event_id' in data['details']


# ============================================================================
# GET /api/invitations - List All Invitations Tests
# ============================================================================

def test_get_invitations_empty(client):
    """Test getting invitations from empty database returns empty array."""
    response = client.get('/api/invitations')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_invitations_with_data(client, app, multiple_events, multiple_participants):
    """Test getting invitations returns all invitations with nested data."""
    # Create test invitations
    with app.app_context():
        invitation1 = Invitation(
            participant_id=multiple_participants[0],
            event_id=multiple_events[0]
        )
        invitation2 = Invitation(
            participant_id=multiple_participants[1],
            event_id=multiple_events[1]
        )
        db.session.add(invitation1)
        db.session.add(invitation2)
        db.session.commit()
    
    response = client.get('/api/invitations')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2
    # Verify nested data is included
    assert 'participant' in data[0]
    assert 'event' in data[0]
    assert data[0]['participant']['name'] == 'John Doe'
    assert data[0]['event']['name'] == 'Marathon 1'


# ============================================================================
# GET /api/invitations?event_id=<id> - Filter by Event Tests
# ============================================================================

def test_get_invitations_filter_by_event(client, app, multiple_events, multiple_participants):
    """Test filtering invitations by event_id returns only matching invitations."""
    # Create invitations for different events
    with app.app_context():
        invitation1 = Invitation(
            participant_id=multiple_participants[0],
            event_id=multiple_events[0]
        )
        invitation2 = Invitation(
            participant_id=multiple_participants[1],
            event_id=multiple_events[0]
        )
        invitation3 = Invitation(
            participant_id=multiple_participants[0],
            event_id=multiple_events[1]
        )
        db.session.add_all([invitation1, invitation2, invitation3])
        db.session.commit()
    
    # Filter by first event
    response = client.get(f'/api/invitations?event_id={multiple_events[0]}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2
    # Verify all returned invitations are for the correct event
    for invitation in data:
        assert invitation['event_id'] == multiple_events[0]
        assert invitation['event']['name'] == 'Marathon 1'


def test_get_invitations_filter_by_nonexistent_event(client):
    """Test filtering by non-existent event returns empty array."""
    response = client.get('/api/invitations?event_id=999')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


# ============================================================================
# GET /api/invitations?participant_id=<id> - Filter by Participant Tests
# ============================================================================

def test_get_invitations_filter_by_participant(client, app, multiple_events, multiple_participants):
    """Test filtering invitations by participant_id returns only matching invitations."""
    # Create invitations for different participants
    with app.app_context():
        invitation1 = Invitation(
            participant_id=multiple_participants[0],
            event_id=multiple_events[0]
        )
        invitation2 = Invitation(
            participant_id=multiple_participants[0],
            event_id=multiple_events[1]
        )
        invitation3 = Invitation(
            participant_id=multiple_participants[1],
            event_id=multiple_events[0]
        )
        db.session.add_all([invitation1, invitation2, invitation3])
        db.session.commit()
    
    # Filter by first participant
    response = client.get(f'/api/invitations?participant_id={multiple_participants[0]}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2
    # Verify all returned invitations are for the correct participant
    for invitation in data:
        assert invitation['participant_id'] == multiple_participants[0]
        assert invitation['participant']['name'] == 'John Doe'


def test_get_invitations_filter_by_nonexistent_participant(client):
    """Test filtering by non-existent participant returns empty array."""
    response = client.get('/api/invitations?participant_id=999')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_invitations_filter_by_both(client, app, multiple_events, multiple_participants):
    """Test filtering by both event_id and participant_id."""
    # Create invitations
    with app.app_context():
        invitation1 = Invitation(
            participant_id=multiple_participants[0],
            event_id=multiple_events[0]
        )
        invitation2 = Invitation(
            participant_id=multiple_participants[0],
            event_id=multiple_events[1]
        )
        invitation3 = Invitation(
            participant_id=multiple_participants[1],
            event_id=multiple_events[0]
        )
        db.session.add_all([invitation1, invitation2, invitation3])
        db.session.commit()
    
    # Filter by both participant and event
    response = client.get(
        f'/api/invitations?participant_id={multiple_participants[0]}&event_id={multiple_events[0]}'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['participant_id'] == multiple_participants[0]
    assert data[0]['event_id'] == multiple_events[0]


# ============================================================================
# DELETE /api/invitations/<id> - Delete Invitation Tests
# ============================================================================

def test_delete_invitation_success(client, app, sample_event, sample_participant):
    """Test deleting existing invitation returns 204."""
    # Create test invitation
    with app.app_context():
        invitation = Invitation(
            participant_id=sample_participant,
            event_id=sample_event
        )
        db.session.add(invitation)
        db.session.commit()
        invitation_id = invitation.id
    
    response = client.delete(f'/api/invitations/{invitation_id}')
    
    assert response.status_code == 204
    assert response.data == b''
    
    # Verify invitation is deleted
    with app.app_context():
        deleted_invitation = db.session.get(Invitation, invitation_id)
        assert deleted_invitation is None


def test_delete_invitation_not_found(client):
    """Test deleting non-existent invitation returns 404."""
    response = client.delete('/api/invitations/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['resource_type'] == 'invitation'
    assert data['id'] == 999


# ============================================================================
# Edge Cases and Integration Tests
# ============================================================================

def test_create_and_retrieve_invitation(client, sample_event, sample_participant):
    """Test that created invitation can be retrieved."""
    # Create invitation
    invitation_data = {
        'participant_id': sample_participant,
        'event_id': sample_event
    }
    create_response = client.post('/api/invitations',
                                 data=json.dumps(invitation_data),
                                 content_type='application/json')
    assert create_response.status_code == 201
    created_invitation = json.loads(create_response.data)
    invitation_id = created_invitation['id']
    
    # Retrieve all invitations and verify it's there
    get_response = client.get('/api/invitations')
    assert get_response.status_code == 200
    invitations = json.loads(get_response.data)
    
    assert len(invitations) == 1
    assert invitations[0]['id'] == invitation_id
    assert invitations[0]['participant_id'] == sample_participant
    assert invitations[0]['event_id'] == sample_event


def test_cascade_delete_event_removes_invitations(client, app, sample_event, sample_participant):
    """Test that deleting an event cascades to delete its invitations."""
    # Create invitation
    with app.app_context():
        invitation = Invitation(
            participant_id=sample_participant,
            event_id=sample_event
        )
        db.session.add(invitation)
        db.session.commit()
        invitation_id = invitation.id
    
    # Delete the event
    response = client.delete(f'/api/events/{sample_event}')
    assert response.status_code == 204
    
    # Verify invitation is also deleted
    with app.app_context():
        deleted_invitation = db.session.get(Invitation, invitation_id)
        assert deleted_invitation is None


def test_cascade_delete_participant_removes_invitations(client, app, sample_event, sample_participant):
    """Test that deleting a participant cascades to delete their invitations."""
    # Create invitation
    with app.app_context():
        invitation = Invitation(
            participant_id=sample_participant,
            event_id=sample_event
        )
        db.session.add(invitation)
        db.session.commit()
        invitation_id = invitation.id
    
    # Delete the participant
    response = client.delete(f'/api/participants/{sample_participant}')
    assert response.status_code == 204
    
    # Verify invitation is also deleted
    with app.app_context():
        deleted_invitation = db.session.get(Invitation, invitation_id)
        assert deleted_invitation is None


def test_multiple_invitations_same_participant(client, app, multiple_events, sample_participant):
    """Test that a participant can have multiple invitations to different events."""
    # Create multiple invitations for same participant
    invitation_data1 = {
        'participant_id': sample_participant,
        'event_id': multiple_events[0]
    }
    invitation_data2 = {
        'participant_id': sample_participant,
        'event_id': multiple_events[1]
    }
    
    response1 = client.post('/api/invitations',
                           data=json.dumps(invitation_data1),
                           content_type='application/json')
    response2 = client.post('/api/invitations',
                           data=json.dumps(invitation_data2),
                           content_type='application/json')
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    
    # Verify both invitations exist
    response = client.get(f'/api/invitations?participant_id={sample_participant}')
    data = json.loads(response.data)
    assert len(data) == 2


def test_multiple_invitations_same_event(client, app, sample_event, multiple_participants):
    """Test that an event can have multiple invitations to different participants."""
    # Create multiple invitations for same event
    invitation_data1 = {
        'participant_id': multiple_participants[0],
        'event_id': sample_event
    }
    invitation_data2 = {
        'participant_id': multiple_participants[1],
        'event_id': sample_event
    }
    
    response1 = client.post('/api/invitations',
                           data=json.dumps(invitation_data1),
                           content_type='application/json')
    response2 = client.post('/api/invitations',
                           data=json.dumps(invitation_data2),
                           content_type='application/json')
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    
    # Verify both invitations exist
    response = client.get(f'/api/invitations?event_id={sample_event}')
    data = json.loads(response.data)
    assert len(data) == 2


def test_invitation_includes_complete_nested_data(client, sample_event, sample_participant):
    """Test that invitation response includes complete participant and event details."""
    invitation_data = {
        'participant_id': sample_participant,
        'event_id': sample_event
    }
    
    response = client.post('/api/invitations',
                          data=json.dumps(invitation_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Verify participant details
    assert data['participant']['name'] == 'John Doe'
    assert data['participant']['email'] == 'john@example.com'
    assert data['participant']['age'] == 30
    
    # Verify event details
    assert data['event']['name'] == 'Test Marathon'
    assert data['event']['location'] == 'Test Location'
    assert data['event']['distance'] == 42.195
