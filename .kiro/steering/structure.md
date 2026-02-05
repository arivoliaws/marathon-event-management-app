# Project Structure

## Directory Layout

```
marathon-registration-app/
├── app/                      # Main application package
│   ├── __init__.py          # App factory, db initialization
│   ├── models.py            # SQLAlchemy models (MarathonEvent, Participant, Invitation)
│   ├── api.py               # REST API blueprint (/api/*)
│   ├── web_routes.py        # Web interface blueprint (HTML pages)
│   └── validation.py        # Input validation functions
├── tests/                    # Test suite
│   ├── test_api_events.py
│   ├── test_api_participants.py
│   ├── test_api_invitations.py
│   ├── test_validation.py
│   └── test_web_*.py        # Web interface tests
├── templates/                # Jinja2 HTML templates
│   ├── base.html
│   ├── events.html
│   ├── participants.html
│   └── invitations.html
├── static/                   # CSS, JS, images
│   └── style.css
├── instance/                 # Instance-specific files (gitignored)
│   └── marathon_registration.db
├── .kiro/                    # Kiro configuration
│   ├── specs/               # Feature specifications
│   └── steering/            # AI assistant guidance
├── config.py                 # Application configuration
├── run.py                    # Application entry point
├── init_db.py               # Database initialization script
└── requirements.txt          # Python dependencies
```

## Architecture Patterns

### Application Factory Pattern

- `create_app()` in `app/__init__.py` creates and configures Flask app
- Enables multiple app instances (testing, development, production)
- Database and blueprints registered within app context

### Blueprint Organization

- **API Blueprint** (`app/api.py`): REST endpoints at `/api/*`
- **Web Blueprint** (`app/web_routes.py`): HTML pages at root paths

### Database Models

Three core models with relationships:
- **MarathonEvent**: Events with name, date, location, distance
- **Participant**: Users with name, email, phone, age
- **Invitation**: Junction table linking participants to events

Cascade deletion: Deleting event/participant removes associated invitations

### Validation Layer

Separate validation module (`app/validation.py`) with functions:
- `validate_event()`: Checks name, future date, location, positive distance
- `validate_participant()`: Checks name, email format, positive age
- `validate_invitation()`: Checks referential integrity (IDs exist)

Returns tuple: `(is_valid: bool, errors: dict)`

## Code Conventions

### Models

- Use `to_dict()` method for JSON serialization
- Include `created_at` and `updated_at` timestamps
- Define bidirectional relationships with `back_populates`

### API Endpoints

- Return JSON with appropriate HTTP status codes:
  - 200: Success (GET, PUT)
  - 201: Created (POST)
  - 204: No Content (DELETE)
  - 400: Validation Error
  - 404: Not Found
  - 500: Server Error
- Use `db.session.get()` for lookups (SQLAlchemy 2.0 syntax)
- Always rollback on exceptions
- Strip whitespace from string inputs

### Testing

- Use pytest fixtures for app, client, and sample data
- In-memory SQLite for test isolation
- Test structure: Arrange-Act-Assert
- Comprehensive coverage: success cases, validation, edge cases, 404s
- Descriptive test names: `test_<action>_<scenario>`

### Error Responses

Consistent JSON error format:
```json
{
  "error": "Error message",
  "details": {"field": "specific error"},
  "resource_type": "event",
  "id": 123
}
```

## File Naming

- Snake_case for Python files and functions
- PascalCase for class names
- Lowercase with hyphens for templates
- Test files prefixed with `test_`
