"""
Unit tests for Participant API endpoints.

Tests cover CRUD operations, validation, error handling, and HTTP status codes.
"""

import pytest
import json
from app import create_app, db
from app.models import Participant


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
def sample_participant_data():
    """Sample valid participant data for testing."""
    return {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '555-1234',
        'age': 30
    }


# ============================================================================
# POST /api/participants - Create Participant Tests
# ============================================================================

def test_create_participant_success(client, sample_participant_data):
    """Test creating a valid participant returns 201 with participant data."""
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == sample_participant_data['name']
    assert data['email'] == sample_participant_data['email']
    assert data['phone'] == sample_participant_data['phone']
    assert data['age'] == sample_participant_data['age']
    assert 'id' in data
    assert 'created_at' in data


def test_create_participant_without_phone(client, sample_participant_data):
    """Test creating participant without phone (optional field) succeeds."""
    del sample_participant_data['phone']
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == sample_participant_data['name']
    assert data['phone'] is None


def test_create_participant_missing_name(client, sample_participant_data):
    """Test creating participant without name returns 400."""
    sample_participant_data['name'] = ''
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data
    assert 'name' in data['details']


def test_create_participant_invalid_email(client, sample_participant_data):
    """Test creating participant with invalid email returns 400."""
    sample_participant_data['email'] = 'invalid-email'
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'email' in data['details']


def test_create_participant_negative_age(client, sample_participant_data):
    """Test creating participant with negative age returns 400."""
    sample_participant_data['age'] = -5
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'age' in data['details']


def test_create_participant_zero_age(client, sample_participant_data):
    """Test creating participant with zero age returns 400."""
    sample_participant_data['age'] = 0
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'age' in data['details']


def test_create_participant_missing_email(client, sample_participant_data):
    """Test creating participant without email returns 400."""
    sample_participant_data['email'] = ''
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'email' in data['details']


# ============================================================================
# GET /api/participants - List All Participants Tests
# ============================================================================

def test_get_participants_empty(client):
    """Test getting participants from empty database returns empty array."""
    response = client.get('/api/participants')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_participants_with_data(client, app):
    """Test getting participants returns all participants in database."""
    # Create test participants
    with app.app_context():
        participant1 = Participant(
            name='Alice Smith',
            email='alice@example.com',
            phone='555-0001',
            age=25
        )
        participant2 = Participant(
            name='Bob Jones',
            email='bob@example.com',
            phone='555-0002',
            age=35
        )
        db.session.add(participant1)
        db.session.add(participant2)
        db.session.commit()
    
    response = client.get('/api/participants')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['name'] == 'Alice Smith'
    assert data[1]['name'] == 'Bob Jones'


# ============================================================================
# GET /api/participants/<id> - Get Single Participant Tests
# ============================================================================

def test_get_participant_success(client, app):
    """Test getting existing participant by ID returns 200 with participant data."""
    # Create test participant
    with app.app_context():
        participant = Participant(
            name='Test User',
            email='test@example.com',
            phone='555-9999',
            age=28
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    
    response = client.get(f'/api/participants/{participant_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == participant_id
    assert data['name'] == 'Test User'
    assert data['email'] == 'test@example.com'


def test_get_participant_not_found(client):
    """Test getting non-existent participant returns 404."""
    response = client.get('/api/participants/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['resource_type'] == 'participant'
    assert data['id'] == 999


# ============================================================================
# PUT /api/participants/<id> - Update Participant Tests
# ============================================================================

def test_update_participant_success(client, app):
    """Test updating existing participant returns 200 with updated data."""
    # Create test participant
    with app.app_context():
        participant = Participant(
            name='Original Name',
            email='original@example.com',
            phone='555-0000',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    
    # Update participant
    update_data = {
        'name': 'Updated Name',
        'phone': '555-1111'
    }
    response = client.put(f'/api/participants/{participant_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Name'
    assert data['phone'] == '555-1111'
    assert data['email'] == 'original@example.com'  # Unchanged
    assert data['age'] == 30  # Unchanged


def test_update_participant_not_found(client):
    """Test updating non-existent participant returns 404."""
    update_data = {'name': 'New Name'}
    response = client.put('/api/participants/999',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['resource_type'] == 'participant'


def test_update_participant_invalid_email(client, app):
    """Test updating participant with invalid email returns 400."""
    # Create test participant
    with app.app_context():
        participant = Participant(
            name='Test User',
            email='test@example.com',
            phone='555-0000',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    
    # Try to update with invalid email
    update_data = {'email': 'invalid-email'}
    response = client.put(f'/api/participants/{participant_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'email' in data['details']


def test_update_participant_invalid_age(client, app):
    """Test updating participant with invalid age returns 400."""
    # Create test participant
    with app.app_context():
        participant = Participant(
            name='Test User',
            email='test@example.com',
            phone='555-0000',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    
    # Try to update with negative age
    update_data = {'age': -10}
    response = client.put(f'/api/participants/{participant_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'details' in data
    assert 'age' in data['details']


# ============================================================================
# DELETE /api/participants/<id> - Delete Participant Tests
# ============================================================================

def test_delete_participant_success(client, app):
    """Test deleting existing participant returns 204."""
    # Create test participant
    with app.app_context():
        participant = Participant(
            name='Test User',
            email='test@example.com',
            phone='555-0000',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    
    response = client.delete(f'/api/participants/{participant_id}')
    
    assert response.status_code == 204
    assert response.data == b''
    
    # Verify participant is deleted
    response = client.get(f'/api/participants/{participant_id}')
    assert response.status_code == 404


def test_delete_participant_not_found(client):
    """Test deleting non-existent participant returns 404."""
    response = client.delete('/api/participants/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['resource_type'] == 'participant'


# ============================================================================
# Edge Cases and Integration Tests
# ============================================================================

def test_create_and_retrieve_participant(client, sample_participant_data):
    """Test that created participant can be retrieved."""
    # Create participant
    create_response = client.post('/api/participants',
                                 data=json.dumps(sample_participant_data),
                                 content_type='application/json')
    assert create_response.status_code == 201
    created_participant = json.loads(create_response.data)
    participant_id = created_participant['id']
    
    # Retrieve participant
    get_response = client.get(f'/api/participants/{participant_id}')
    assert get_response.status_code == 200
    retrieved_participant = json.loads(get_response.data)
    
    assert retrieved_participant['id'] == participant_id
    assert retrieved_participant['name'] == sample_participant_data['name']
    assert retrieved_participant['email'] == sample_participant_data['email']


def test_update_persists_changes(client, app):
    """Test that updates are persisted to database."""
    # Create participant
    with app.app_context():
        participant = Participant(
            name='Original',
            email='original@example.com',
            phone='555-0000',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        participant_id = participant.id
    
    # Update participant
    update_data = {'name': 'Updated'}
    client.put(f'/api/participants/{participant_id}',
              data=json.dumps(update_data),
              content_type='application/json')
    
    # Verify update persisted
    response = client.get(f'/api/participants/{participant_id}')
    data = json.loads(response.data)
    assert data['name'] == 'Updated'


def test_whitespace_trimming(client, sample_participant_data):
    """Test that whitespace is trimmed from string fields."""
    sample_participant_data['name'] = '  John Doe  '
    sample_participant_data['email'] = '  john.doe@example.com  '
    sample_participant_data['phone'] = '  555-1234  '
    
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'
    assert data['email'] == 'john.doe@example.com'
    assert data['phone'] == '555-1234'


def test_various_email_formats(client, sample_participant_data):
    """Test that various valid email formats are accepted."""
    valid_emails = [
        'user@example.com',
        'user.name@example.com',
        'user+tag@example.co.uk',
        'user_name@example-domain.com',
        'user123@test.org'
    ]
    
    for idx, email in enumerate(valid_emails):
        sample_participant_data['email'] = email
        sample_participant_data['name'] = f'User {idx}'
        
        response = client.post('/api/participants',
                              data=json.dumps(sample_participant_data),
                              content_type='application/json')
        
        assert response.status_code == 201, f"Failed for email: {email}"
        data = json.loads(response.data)
        assert data['email'] == email


def test_invalid_email_formats(client, sample_participant_data):
    """Test that invalid email formats are rejected."""
    invalid_emails = [
        'notanemail',
        '@example.com',
        'user@',
        'user @example.com',
        'user@example'
    ]
    
    for email in invalid_emails:
        sample_participant_data['email'] = email
        
        response = client.post('/api/participants',
                              data=json.dumps(sample_participant_data),
                              content_type='application/json')
        
        assert response.status_code == 400, f"Should fail for email: {email}"
        data = json.loads(response.data)
        assert 'email' in data['details']


def test_boundary_age_values(client, sample_participant_data):
    """Test boundary values for age field."""
    # Age = 1 should be valid (minimum positive integer)
    sample_participant_data['age'] = 1
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    assert response.status_code == 201
    
    # Age = 150 should be valid (high but positive)
    sample_participant_data['email'] = 'another@example.com'
    sample_participant_data['age'] = 150
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    assert response.status_code == 201


def test_empty_phone_vs_null_phone(client, sample_participant_data):
    """Test that empty phone string is treated as null."""
    sample_participant_data['phone'] = ''
    response = client.post('/api/participants',
                          data=json.dumps(sample_participant_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['phone'] is None
