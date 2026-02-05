"""
Unit tests for Marathon Event API endpoints.

Tests cover CRUD operations, validation, error handling, and HTTP status codes.
"""

import pytest
import json
from datetime import date, timedelta
from app import create_app, db
from app.models import MarathonEvent


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
def sample_event_data():
    """Sample valid event data for testing."""
    future_date = (date.today() + timedelta(days=30)).isoformat()
    return {
        'name': 'Boston Marathon',
        'date': future_date,
        'location': 'Boston, MA',
        'distance': 42.195
    }


# ============================================================================
# POST /api/events - Create Event Tests
# ============================================================================

def test_create_event_success(client, sample_event_data):
    """Test creating a valid event returns 201 with event data."""
    response = client.post('/api/events',
                          data=json.dumps(sample_event_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == sample_event_data['name']
    assert data['location'] == sample_event_data['location']
    assert data['distance'] == sample_event_data['distance']
    assert 'id' in data
    assert 'created_at' in data


def test_create_event_missing_name(client, sample_event_data):
    """Test creating event without name returns 400."""
    sample_event_data['name'] = ''
    response = client.post('/api/events',
                          data=json.dumps(sample_event_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data
    assert 'name' in data['details']


def test_create_event_past_date(client, sample_event_data):
    """Test creating event with past date returns 400."""
    sample_event_data['date'] = '2020-01-01'
    response = client.post('/api/events',
                          data=json.dumps(sample_event_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'date' in data['details']


def test_create_event_negative_distance(client, sample_event_data):
    """Test creating event with negative distance returns 400."""
    sample_event_data['distance'] = -10
    response = client.post('/api/events',
                          data=json.dumps(sample_event_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'distance' in data['details']


def test_create_event_missing_location(client, sample_event_data):
    """Test creating event without location returns 400."""
    sample_event_data['location'] = ''
    response = client.post('/api/events',
                          data=json.dumps(sample_event_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'location' in data['details']


# ============================================================================
# GET /api/events - List All Events Tests
# ============================================================================

def test_get_events_empty(client):
    """Test getting events from empty database returns empty array."""
    response = client.get('/api/events')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_events_with_data(client, app, sample_event_data):
    """Test getting events returns all events in database."""
    # Create test events
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
    
    response = client.get('/api/events')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['name'] == 'Marathon 1'
    assert data[1]['name'] == 'Marathon 2'


# ============================================================================
# GET /api/events/<id> - Get Single Event Tests
# ============================================================================

def test_get_event_success(client, app):
    """Test getting existing event by ID returns 200 with event data."""
    # Create test event
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
    
    response = client.get(f'/api/events/{event_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == event_id
    assert data['name'] == 'Test Marathon'
    assert data['location'] == 'Test Location'


def test_get_event_not_found(client):
    """Test getting non-existent event returns 404."""
    response = client.get('/api/events/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['resource_type'] == 'event'
    assert data['id'] == 999


# ============================================================================
# PUT /api/events/<id> - Update Event Tests
# ============================================================================

def test_update_event_success(client, app):
    """Test updating existing event returns 200 with updated data."""
    # Create test event
    with app.app_context():
        event = MarathonEvent(
            name='Original Name',
            date=date.today() + timedelta(days=30),
            location='Original Location',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    # Update event
    update_data = {
        'name': 'Updated Name',
        'location': 'Updated Location'
    }
    response = client.put(f'/api/events/{event_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Name'
    assert data['location'] == 'Updated Location'
    assert data['distance'] == 42.195  # Unchanged


def test_update_event_not_found(client):
    """Test updating non-existent event returns 404."""
    update_data = {'name': 'New Name'}
    response = client.put('/api/events/999',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['resource_type'] == 'event'


def test_update_event_invalid_data(client, app):
    """Test updating event with invalid data returns 400."""
    # Create test event
    with app.app_context():
        event = MarathonEvent(
            name='Test Event',
            date=date.today() + timedelta(days=30),
            location='Test Location',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    # Try to update with invalid distance
    update_data = {'distance': -10}
    response = client.put(f'/api/events/{event_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'distance' in data['details']


# ============================================================================
# DELETE /api/events/<id> - Delete Event Tests
# ============================================================================

def test_delete_event_success(client, app):
    """Test deleting existing event returns 204."""
    # Create test event
    with app.app_context():
        event = MarathonEvent(
            name='Test Event',
            date=date.today() + timedelta(days=30),
            location='Test Location',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    response = client.delete(f'/api/events/{event_id}')
    
    assert response.status_code == 204
    assert response.data == b''
    
    # Verify event is deleted
    response = client.get(f'/api/events/{event_id}')
    assert response.status_code == 404


def test_delete_event_not_found(client):
    """Test deleting non-existent event returns 404."""
    response = client.delete('/api/events/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['resource_type'] == 'event'


# ============================================================================
# Edge Cases and Integration Tests
# ============================================================================

def test_create_and_retrieve_event(client, sample_event_data):
    """Test that created event can be retrieved."""
    # Create event
    create_response = client.post('/api/events',
                                 data=json.dumps(sample_event_data),
                                 content_type='application/json')
    assert create_response.status_code == 201
    created_event = json.loads(create_response.data)
    event_id = created_event['id']
    
    # Retrieve event
    get_response = client.get(f'/api/events/{event_id}')
    assert get_response.status_code == 200
    retrieved_event = json.loads(get_response.data)
    
    assert retrieved_event['id'] == event_id
    assert retrieved_event['name'] == sample_event_data['name']


def test_update_persists_changes(client, app):
    """Test that updates are persisted to database."""
    # Create event
    with app.app_context():
        event = MarathonEvent(
            name='Original',
            date=date.today() + timedelta(days=30),
            location='Original Location',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    # Update event
    update_data = {'name': 'Updated'}
    client.put(f'/api/events/{event_id}',
              data=json.dumps(update_data),
              content_type='application/json')
    
    # Verify update persisted
    response = client.get(f'/api/events/{event_id}')
    data = json.loads(response.data)
    assert data['name'] == 'Updated'


def test_whitespace_trimming(client, sample_event_data):
    """Test that whitespace is trimmed from string fields."""
    sample_event_data['name'] = '  Boston Marathon  '
    sample_event_data['location'] = '  Boston, MA  '
    
    response = client.post('/api/events',
                          data=json.dumps(sample_event_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Boston Marathon'
    assert data['location'] == 'Boston, MA'
