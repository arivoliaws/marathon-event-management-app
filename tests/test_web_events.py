"""
Unit tests for event web routes.
Tests the event management web interface including create, update, and delete operations.
"""

import pytest
import json
from datetime import date, timedelta
from app import create_app, db
from app.models import MarathonEvent


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


def test_events_page_displays_all_events(client, app):
    """
    Test that GET /events returns correct template with all events.
    Requirements: 1.2, 6.1
    """
    with app.app_context():
        # Create test events
        event1 = MarathonEvent(
            name='Boston Marathon',
            date=date.today() + timedelta(days=30),
            location='Boston, MA',
            distance=42.195
        )
        event2 = MarathonEvent(
            name='NYC Marathon',
            date=date.today() + timedelta(days=60),
            location='New York, NY',
            distance=42.195
        )
        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()
    
    response = client.get('/events')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    assert 'Boston Marathon' in html
    assert 'NYC Marathon' in html
    assert 'Boston, MA' in html
    assert 'New York, NY' in html


def test_events_page_shows_empty_state(client):
    """
    Test that events page shows empty state when no events exist.
    Requirements: 6.1
    """
    response = client.get('/events')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    assert 'No events yet' in html or 'empty' in html.lower()


def test_create_event_with_valid_data_ajax(client, app):
    """
    Test POST /events/create with valid data via AJAX.
    Requirements: 1.1, 6.1, 6.4
    """
    future_date = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    response = client.post('/events/create', data={
        'name': 'Test Marathon',
        'date': future_date,
        'location': 'Test City',
        'distance': '42.195'
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['event']['name'] == 'Test Marathon'
    assert data['event']['location'] == 'Test City'
    assert data['event']['distance'] == 42.195
    
    # Verify event was created in database
    with app.app_context():
        event = MarathonEvent.query.filter_by(name='Test Marathon').first()
        assert event is not None
        assert event.location == 'Test City'


def test_create_event_with_invalid_data_ajax(client):
    """
    Test POST /events/create with invalid data via AJAX returns validation errors.
    Requirements: 1.5, 6.5
    """
    response = client.post('/events/create', data={
        'name': '',  # Empty name
        'date': '2020-01-01',  # Past date
        'location': '',  # Empty location
        'distance': '-5'  # Negative distance
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'errors' in data
    assert 'name' in data['errors']
    assert 'date' in data['errors']
    assert 'location' in data['errors']
    assert 'distance' in data['errors']


def test_update_event_with_valid_data_ajax(client, app):
    """
    Test POST /events/<id>/update with valid data via AJAX.
    Requirements: 1.3, 6.1, 6.4
    """
    with app.app_context():
        # Create initial event
        event = MarathonEvent(
            name='Original Name',
            date=date.today() + timedelta(days=30),
            location='Original Location',
            distance=21.0975
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    future_date = (date.today() + timedelta(days=60)).strftime('%Y-%m-%d')
    
    response = client.post(f'/events/{event_id}/update', data={
        'name': 'Updated Name',
        'date': future_date,
        'location': 'Updated Location',
        'distance': '42.195'
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['event']['name'] == 'Updated Name'
    assert data['event']['location'] == 'Updated Location'
    
    # Verify event was updated in database
    with app.app_context():
        event = db.session.get(MarathonEvent, event_id)
        assert event.name == 'Updated Name'
        assert event.location == 'Updated Location'
        assert event.distance == 42.195


def test_update_nonexistent_event_ajax(client):
    """
    Test POST /events/<id>/update with non-existent event ID.
    Requirements: 6.1
    """
    future_date = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    response = client.post('/events/9999/update', data={
        'name': 'Test',
        'date': future_date,
        'location': 'Test',
        'distance': '42.195'
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False


def test_update_event_with_invalid_data_ajax(client, app):
    """
    Test POST /events/<id>/update with invalid data returns validation errors.
    Requirements: 1.5, 6.5
    """
    with app.app_context():
        # Create initial event
        event = MarathonEvent(
            name='Test Event',
            date=date.today() + timedelta(days=30),
            location='Test Location',
            distance=21.0975
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    response = client.post(f'/events/{event_id}/update', data={
        'name': '',  # Empty name
        'date': '2020-01-01',  # Past date
        'location': '',  # Empty location
        'distance': '0'  # Invalid distance
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'errors' in data


def test_delete_event_ajax(client, app):
    """
    Test POST /events/<id>/delete via AJAX.
    Requirements: 1.4, 6.1, 6.4
    """
    with app.app_context():
        # Create event to delete
        event = MarathonEvent(
            name='Event to Delete',
            date=date.today() + timedelta(days=30),
            location='Test Location',
            distance=21.0975
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id
    
    response = client.post(f'/events/{event_id}/delete',
                          headers={'X-Requested-With': 'XMLHttpRequest'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify event was deleted from database
    with app.app_context():
        event = db.session.get(MarathonEvent, event_id)
        assert event is None


def test_delete_nonexistent_event_ajax(client):
    """
    Test POST /events/<id>/delete with non-existent event ID.
    Requirements: 6.1
    """
    response = client.post('/events/9999/delete',
                          headers={'X-Requested-With': 'XMLHttpRequest'})
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False


def test_events_page_has_create_form(client):
    """
    Test that events page includes a create form.
    Requirements: 6.1
    """
    response = client.get('/events')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    assert 'Create' in html or 'create' in html
    assert 'name' in html.lower()
    assert 'date' in html.lower()
    assert 'location' in html.lower()
    assert 'distance' in html.lower()


def test_events_page_has_edit_and_delete_buttons(client, app):
    """
    Test that events page includes edit and delete buttons for each event.
    Requirements: 6.1
    """
    with app.app_context():
        # Create test event
        event = MarathonEvent(
            name='Test Event',
            date=date.today() + timedelta(days=30),
            location='Test Location',
            distance=21.0975
        )
        db.session.add(event)
        db.session.commit()
    
    response = client.get('/events')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    assert 'Edit' in html or 'edit' in html
    assert 'Delete' in html or 'delete' in html
