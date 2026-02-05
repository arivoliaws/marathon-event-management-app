"""
Unit tests for validation functions.

Tests specific examples and edge cases for event, participant, and invitation validation.
"""

import pytest
from datetime import date, timedelta
from app import create_app, db
from app.models import MarathonEvent, Participant
from app.validation import validate_event, validate_participant, validate_invitation


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
def app_context(app):
    """Create an application context for tests."""
    with app.app_context():
        yield


class TestEventValidation:
    """Test cases for validate_event function."""
    
    def test_valid_event(self):
        """Test validation passes for valid event data."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is True
        assert errors == {}
    
    def test_empty_name(self):
        """Test validation fails when name is empty."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': '',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'name' in errors
        assert 'required' in errors['name'].lower()
    
    def test_whitespace_only_name(self):
        """Test validation fails when name is only whitespace."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': '   ',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_missing_name(self):
        """Test validation fails when name is missing."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_past_date(self):
        """Test validation fails when date is in the past."""
        past_date = date.today() - timedelta(days=1)
        data = {
            'name': 'Boston Marathon',
            'date': past_date,
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'date' in errors
        assert 'future' in errors['date'].lower()
    
    def test_current_date(self):
        """Test validation fails when date is today."""
        data = {
            'name': 'Boston Marathon',
            'date': date.today(),
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'date' in errors
    
    def test_missing_date(self):
        """Test validation fails when date is missing."""
        data = {
            'name': 'Boston Marathon',
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'date' in errors
    
    def test_string_date_valid(self):
        """Test validation handles string dates correctly."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date.strftime('%Y-%m-%d'),
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is True
        assert errors == {}
    
    def test_invalid_date_format(self):
        """Test validation fails for invalid date format."""
        data = {
            'name': 'Boston Marathon',
            'date': '2024-13-45',  # Invalid date
            'location': 'Boston, MA',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'date' in errors
    
    def test_empty_location(self):
        """Test validation fails when location is empty."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': '',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'location' in errors
    
    def test_whitespace_only_location(self):
        """Test validation fails when location is only whitespace."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': '   ',
            'distance': 42.195
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'location' in errors
    
    def test_zero_distance(self):
        """Test validation fails when distance is zero."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 0
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'distance' in errors
        assert 'positive' in errors['distance'].lower()
    
    def test_negative_distance(self):
        """Test validation fails when distance is negative."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': -5.0
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'distance' in errors
    
    def test_small_positive_distance(self):
        """Test validation passes for small positive distance."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Fun Run',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 0.1
        }
        is_valid, errors = validate_event(data)
        assert is_valid is True
        assert errors == {}
    
    def test_missing_distance(self):
        """Test validation fails when distance is missing."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': 'Boston, MA'
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'distance' in errors
    
    def test_invalid_distance_type(self):
        """Test validation fails when distance is not a number."""
        future_date = date.today() + timedelta(days=30)
        data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 'not a number'
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'distance' in errors
    
    def test_multiple_errors(self):
        """Test validation returns all errors when multiple fields are invalid."""
        data = {
            'name': '',
            'date': date.today(),
            'location': '',
            'distance': -1
        }
        is_valid, errors = validate_event(data)
        assert is_valid is False
        assert 'name' in errors
        assert 'date' in errors
        assert 'location' in errors
        assert 'distance' in errors


class TestParticipantValidation:
    """Test cases for validate_participant function."""
    
    def test_valid_participant(self):
        """Test validation passes for valid participant data."""
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is True
        assert errors == {}
    
    def test_empty_name(self):
        """Test validation fails when name is empty."""
        data = {
            'name': '',
            'email': 'john.doe@example.com',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_whitespace_only_name(self):
        """Test validation fails when name is only whitespace."""
        data = {
            'name': '   ',
            'email': 'john.doe@example.com',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_missing_email(self):
        """Test validation fails when email is missing."""
        data = {
            'name': 'John Doe',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_empty_email(self):
        """Test validation fails when email is empty."""
        data = {
            'name': 'John Doe',
            'email': '',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_invalid_email_no_at(self):
        """Test validation fails for email without @ symbol."""
        data = {
            'name': 'John Doe',
            'email': 'johndoe.example.com',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_invalid_email_no_domain(self):
        """Test validation fails for email without domain."""
        data = {
            'name': 'John Doe',
            'email': 'john@',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_invalid_email_no_tld(self):
        """Test validation fails for email without top-level domain."""
        data = {
            'name': 'John Doe',
            'email': 'john@example',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_valid_email_with_plus(self):
        """Test validation passes for email with plus sign."""
        data = {
            'name': 'John Doe',
            'email': 'john+test@example.com',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is True
        assert errors == {}
    
    def test_valid_email_with_subdomain(self):
        """Test validation passes for email with subdomain."""
        data = {
            'name': 'John Doe',
            'email': 'john@mail.example.com',
            'age': 30
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is True
        assert errors == {}
    
    def test_zero_age(self):
        """Test validation fails when age is zero."""
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'age': 0
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'age' in errors
        assert 'positive' in errors['age'].lower()
    
    def test_negative_age(self):
        """Test validation fails when age is negative."""
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'age': -5
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'age' in errors
    
    def test_age_one(self):
        """Test validation passes when age is 1."""
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'age': 1
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is True
        assert errors == {}
    
    def test_missing_age(self):
        """Test validation fails when age is missing."""
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com'
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'age' in errors
    
    def test_invalid_age_type(self):
        """Test validation fails when age is not a number."""
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'age': 'thirty'
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'age' in errors
    
    def test_multiple_errors(self):
        """Test validation returns all errors when multiple fields are invalid."""
        data = {
            'name': '',
            'email': 'invalid-email',
            'age': -1
        }
        is_valid, errors = validate_participant(data)
        assert is_valid is False
        assert 'name' in errors
        assert 'email' in errors
        assert 'age' in errors


class TestInvitationValidation:
    """Test cases for validate_invitation function."""
    
    def test_valid_invitation(self, app_context):
        """Test validation passes when both participant and event exist."""
        # Create a participant
        participant = Participant(
            name='John Doe',
            email='john@example.com',
            age=30
        )
        db.session.add(participant)
        
        # Create an event
        event = MarathonEvent(
            name='Boston Marathon',
            date=date.today() + timedelta(days=30),
            location='Boston, MA',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        
        is_valid, errors = validate_invitation(participant.id, event.id)
        assert is_valid is True
        assert errors == {}
    
    def test_nonexistent_participant(self, app_context):
        """Test validation fails when participant doesn't exist."""
        # Create an event
        event = MarathonEvent(
            name='Boston Marathon',
            date=date.today() + timedelta(days=30),
            location='Boston, MA',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        
        is_valid, errors = validate_invitation(99999, event.id)
        assert is_valid is False
        assert 'participant_id' in errors
        assert 'not found' in errors['participant_id'].lower()
    
    def test_nonexistent_event(self, app_context):
        """Test validation fails when event doesn't exist."""
        # Create a participant
        participant = Participant(
            name='John Doe',
            email='john@example.com',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        
        is_valid, errors = validate_invitation(participant.id, 99999)
        assert is_valid is False
        assert 'event_id' in errors
        assert 'not found' in errors['event_id'].lower()
    
    def test_both_nonexistent(self, app_context):
        """Test validation fails when both participant and event don't exist."""
        is_valid, errors = validate_invitation(99999, 99999)
        assert is_valid is False
        assert 'participant_id' in errors
        assert 'event_id' in errors
    
    def test_missing_participant_id(self, app_context):
        """Test validation fails when participant_id is None."""
        # Create an event
        event = MarathonEvent(
            name='Boston Marathon',
            date=date.today() + timedelta(days=30),
            location='Boston, MA',
            distance=42.195
        )
        db.session.add(event)
        db.session.commit()
        
        is_valid, errors = validate_invitation(None, event.id)
        assert is_valid is False
        assert 'participant_id' in errors
    
    def test_missing_event_id(self, app_context):
        """Test validation fails when event_id is None."""
        # Create a participant
        participant = Participant(
            name='John Doe',
            email='john@example.com',
            age=30
        )
        db.session.add(participant)
        db.session.commit()
        
        is_valid, errors = validate_invitation(participant.id, None)
        assert is_valid is False
        assert 'event_id' in errors
    
    def test_both_ids_missing(self, app_context):
        """Test validation fails when both IDs are None."""
        is_valid, errors = validate_invitation(None, None)
        assert is_valid is False
        assert 'participant_id' in errors
        assert 'event_id' in errors
