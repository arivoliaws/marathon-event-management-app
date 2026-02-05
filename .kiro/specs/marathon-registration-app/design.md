# Design Document: Marathon Registration Web Application

## Overview

The Marathon Registration Web Application is a Flask-based web application that provides both a web interface and REST API for managing marathon events, participants, and invitations. The system uses SQLAlchemy ORM for database operations with SQLite as the database backend, ensuring immediate persistence of all changes without requiring server restarts.

The application follows a three-tier architecture:
- **Presentation Layer**: HTML templates using Jinja2 for server-side rendering
- **Application Layer**: Flask routes handling both web pages and REST API endpoints
- **Data Layer**: SQLAlchemy models with SQLite database

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
│  (HTML Forms, AJAX requests for real-time updates)     │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ HTTP/HTTPS
                 │
┌────────────────▼────────────────────────────────────────┐
│              Flask Application                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Web Routes (HTML Templates)              │  │
│  │  - Event Management Pages                        │  │
│  │  - Participant Management Pages                  │  │
│  │  - Invitation Management Pages                   │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         REST API Routes (JSON)                   │  │
│  │  - /api/events (CRUD)                            │  │
│  │  - /api/participants (CRUD)                      │  │
│  │  - /api/invitations (CRUD)                       │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Business Logic Layer                     │  │
│  │  - Validation Functions                          │  │
│  │  - Data Processing                               │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ SQLAlchemy ORM
                 │
┌────────────────▼────────────────────────────────────────┐
│              SQLite Database                            │
│  - marathon_events table                                │
│  - participants table                                   │
│  - invitations table                                    │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Web Framework**: Flask 3.x
- **ORM**: SQLAlchemy 2.x
- **Database**: SQLite (for development and production)
- **Template Engine**: Jinja2 (included with Flask)
- **Frontend**: HTML5, CSS3, JavaScript (for AJAX updates)
- **Validation**: WTForms or custom validation functions

## Components and Interfaces

### 1. Data Models (SQLAlchemy)

#### MarathonEvent Model
```python
class MarathonEvent:
    id: Integer (Primary Key, Auto-increment)
    name: String(200, not null)
    date: Date (not null)
    location: String(200, not null)
    distance: Float (not null, positive)
    created_at: DateTime (default=now)
    updated_at: DateTime (default=now, onupdate=now)
```

#### Participant Model
```python
class Participant:
    id: Integer (Primary Key, Auto-increment)
    name: String(200, not null)
    email: String(200, not null, unique)
    phone: String(20, nullable)
    age: Integer (not null, positive)
    created_at: DateTime (default=now)
    updated_at: DateTime (default=now, onupdate=now)
```

#### Invitation Model
```python
class Invitation:
    id: Integer (Primary Key, Auto-increment)
    participant_id: Integer (Foreign Key -> participants.id, not null)
    event_id: Integer (Foreign Key -> marathon_events.id, not null)
    sent_at: DateTime (default=now)
    
    # Relationships
    participant: Relationship to Participant
    event: Relationship to MarathonEvent
```

### 2. REST API Endpoints

#### Marathon Events API
- `POST /api/events` - Create new event
  - Request: JSON with name, date, location, distance
  - Response: 201 Created with event JSON
  - Error: 400 Bad Request if validation fails

- `GET /api/events` - List all events
  - Response: 200 OK with array of event JSON objects

- `GET /api/events/<id>` - Get specific event
  - Response: 200 OK with event JSON
  - Error: 404 Not Found if event doesn't exist

- `PUT /api/events/<id>` - Update event
  - Request: JSON with fields to update
  - Response: 200 OK with updated event JSON
  - Error: 404 Not Found, 400 Bad Request

- `DELETE /api/events/<id>` - Delete event
  - Response: 204 No Content
  - Error: 404 Not Found

#### Participants API
- `POST /api/participants` - Create new participant
- `GET /api/participants` - List all participants
- `GET /api/participants/<id>` - Get specific participant
- `PUT /api/participants/<id>` - Update participant
- `DELETE /api/participants/<id>` - Delete participant

(Same response patterns as Events API)

#### Invitations API
- `POST /api/invitations` - Create new invitation
  - Request: JSON with participant_id, event_id
  - Response: 201 Created with invitation JSON (includes participant and event details)
  - Error: 400 Bad Request if participant or event doesn't exist

- `GET /api/invitations` - List all invitations
  - Response: 200 OK with array of invitation JSON objects (includes nested participant and event data)

- `GET /api/invitations?event_id=<id>` - List invitations for specific event
- `GET /api/invitations?participant_id=<id>` - List invitations for specific participant

- `DELETE /api/invitations/<id>` - Delete invitation
  - Response: 204 No Content
  - Error: 404 Not Found

### 3. Web Interface Routes

#### Event Management Pages
- `GET /` or `GET /events` - Display all events with create/edit/delete forms
- `POST /events/create` - Handle event creation form submission
- `POST /events/<id>/update` - Handle event update form submission
- `POST /events/<id>/delete` - Handle event deletion

#### Participant Management Pages
- `GET /participants` - Display all participants with create/edit/delete forms
- `POST /participants/create` - Handle participant creation form submission
- `POST /participants/<id>/update` - Handle participant update form submission
- `POST /participants/<id>/delete` - Handle participant deletion

#### Invitation Management Pages
- `GET /invitations` - Display all invitations with create/delete forms
- `POST /invitations/create` - Handle invitation creation form submission
- `POST /invitations/<id>/delete` - Handle invitation deletion

### 4. Validation Functions

#### validate_event(data)
- Validates event data before database operations
- Checks: name is non-empty, date is valid and in future, location is non-empty, distance is positive
- Returns: (is_valid: bool, errors: dict)

#### validate_participant(data)
- Validates participant data before database operations
- Checks: name is non-empty, email format is valid, age is positive integer
- Returns: (is_valid: bool, errors: dict)

#### validate_invitation(participant_id, event_id)
- Validates invitation data before database operations
- Checks: participant exists, event exists
- Returns: (is_valid: bool, errors: dict)

## Data Models

### Database Schema

```sql
CREATE TABLE marathon_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(200) NOT NULL,
    distance FLOAT NOT NULL CHECK(distance > 0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    phone VARCHAR(20),
    age INTEGER NOT NULL CHECK(age > 0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invitations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES marathon_events(id) ON DELETE CASCADE
);
```

### Data Relationships

- **Invitation → Participant**: Many-to-One (many invitations can reference one participant)
- **Invitation → MarathonEvent**: Many-to-One (many invitations can reference one event)
- **Participant ↔ MarathonEvent**: Many-to-Many (through Invitation table)

### Real-Time Persistence Strategy

All database operations use SQLAlchemy's session management with immediate commits:

```python
# Create operation
db.session.add(new_object)
db.session.commit()

# Update operation
object.field = new_value
db.session.commit()

# Delete operation
db.session.delete(object)
db.session.commit()
```

Error handling with rollback:
```python
try:
    # database operation
    db.session.commit()
except Exception as e:
    db.session.rollback()
    # return error response
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### CRUD Operations Properties

**Property 1: Create operation persistence**
*For any* valid entity (event, participant, or invitation), creating it through the API should result in that entity being retrievable from the database with all its attributes preserved.
**Validates: Requirements 1.1, 2.1, 3.1, 5.1**

**Property 2: Read all operation completeness**
*For any* set of entities in the database, querying for all entities of that type should return exactly that set with no additions or omissions.
**Validates: Requirements 1.2, 2.2, 3.2**

**Property 3: Update operation persistence**
*For any* existing entity and any valid update data, updating the entity should result in the modified entity being retrievable from the database with the updated attributes.
**Validates: Requirements 1.3, 2.3, 5.1**

**Property 4: Delete operation removal**
*For any* existing entity, deleting it should result in that entity no longer being retrievable from the database.
**Validates: Requirements 1.4, 2.4, 3.5, 5.1**

### Filtering Properties

**Property 5: Event-based invitation filtering**
*For any* event and any set of invitations in the database, querying invitations by event ID should return only invitations where the event_id matches the specified event, and should include all such invitations.
**Validates: Requirements 3.3**

**Property 6: Participant-based invitation filtering**
*For any* participant and any set of invitations in the database, querying invitations by participant ID should return only invitations where the participant_id matches the specified participant, and should include all such invitations.
**Validates: Requirements 3.4**

### Validation Properties

**Property 7: Event validation correctness**
*For any* event data, the validation function should reject it if and only if: name is empty, date is not a valid future date, location is empty, or distance is not a positive number. Valid data should pass validation.
**Validates: Requirements 1.5, 7.1**

**Property 8: Participant validation correctness**
*For any* participant data, the validation function should reject it if and only if: name is empty, email does not match valid email format, or age is not a positive integer. Valid data should pass validation.
**Validates: Requirements 2.5, 7.2**

**Property 9: Invitation referential integrity**
*For any* invitation data, the validation function should reject it if and only if the referenced participant or event does not exist in the database. Valid references should pass validation.
**Validates: Requirements 7.3**

### HTTP Response Properties

**Property 10: Successful operation status codes**
*For any* successful create operation, the API should return status 201; for any successful read operation, status 200; for any successful update operation, status 200; for any successful delete operation, status 204.
**Validates: Requirements 4.4**

**Property 11: Invalid input status codes**
*For any* API request with invalid input data (failing validation), the API should return status 400 with error details describing which fields are invalid.
**Validates: Requirements 4.5, 7.4**

**Property 12: Non-existent resource status codes**
*For any* API request referencing a resource ID that does not exist in the database, the API should return status 404.
**Validates: Requirements 4.6**

### Transaction Properties

**Property 13: Transaction rollback on failure**
*For any* database operation that encounters an error during execution, the database state should remain unchanged (rollback) and an error message should be returned.
**Validates: Requirements 5.4**

## Error Handling

### Validation Errors
- All validation errors return HTTP 400 with JSON response containing field-specific error messages
- Format: `{"error": "Validation failed", "details": {"field_name": "error message"}}`

### Not Found Errors
- Resource not found errors return HTTP 404 with JSON response
- Format: `{"error": "Resource not found", "resource_type": "event|participant|invitation", "id": <id>}`

### Database Errors
- Database operation failures trigger automatic rollback
- Return HTTP 500 with generic error message (avoid exposing internal details)
- Format: `{"error": "An error occurred while processing your request"}`
- Log detailed error information server-side for debugging

### Referential Integrity Errors
- Attempting to create invitation with non-existent participant or event returns HTTP 400
- Format: `{"error": "Invalid reference", "details": {"participant_id": "Participant not found"}}`

## Testing Strategy

### Dual Testing Approach

The application will use both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs using randomized test data

Both testing approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing

**Framework**: We will use **Hypothesis** (Python property-based testing library) for implementing property tests.

**Configuration**:
- Each property test will run a minimum of 100 iterations with randomized inputs
- Each test will be tagged with a comment referencing its design document property
- Tag format: `# Feature: marathon-registration-app, Property N: <property text>`

**Test Coverage**:
- Property 1-4: CRUD operation tests with random valid entity data
- Property 5-6: Filtering tests with random database states
- Property 7-9: Validation tests with random valid and invalid inputs
- Property 10-12: HTTP response tests with random request scenarios
- Property 13: Transaction rollback tests with simulated failures

### Unit Testing

**Framework**: pytest for Python unit tests

**Focus Areas**:
- Specific examples demonstrating correct behavior (e.g., creating a specific event)
- Edge cases (e.g., empty database queries, boundary values for age/distance)
- Error conditions (e.g., duplicate email registration, invalid date formats)
- Integration between components (e.g., cascade deletion of invitations when event is deleted)

**Test Organization**:
- `tests/test_models.py` - SQLAlchemy model tests
- `tests/test_api.py` - REST API endpoint tests
- `tests/test_validation.py` - Validation function tests
- `tests/test_web_routes.py` - Web interface route tests
- `tests/test_properties.py` - Property-based tests

### Test Data Generation

For property-based tests, we will create generators for:
- Random valid events (with future dates, positive distances)
- Random valid participants (with valid email formats, positive ages)
- Random valid invitations (with existing participant and event IDs)
- Random invalid data (for validation testing)

### Integration Testing

- Test complete workflows: create event → create participant → send invitation
- Test cascade deletions: delete event → verify invitations are removed
- Test concurrent operations: simulate multiple simultaneous requests
- Test database persistence: create data → restart application → verify data exists

### Manual Testing Checklist

While automated tests cover functional correctness, manual testing should verify:
- Web interface displays correctly in different browsers
- Forms provide good user experience
- Error messages are clear and helpful
- Real-time updates work without page refresh (AJAX functionality)
