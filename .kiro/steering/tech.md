# Technology Stack

## Core Framework

- **Flask 3.0.0**: Web framework and application server
- **Flask-SQLAlchemy 3.1.1**: ORM integration
- **SQLAlchemy 2.0.36**: Database ORM (using 2.0 syntax with `db.session.get()`)
- **WTForms 3.1.1**: Form handling and validation

## Database

- **SQLite**: Default database (file-based at `instance/marathon_registration.db`)
- Configurable via `SQLALCHEMY_DATABASE_URI` environment variable

## Testing

- **pytest 7.4.3**: Test framework
- **hypothesis 6.92.1**: Property-based testing library
- In-memory SQLite database for test isolation

## Python Version

- Python 3.x (modern async/await compatible)

## Common Commands

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (creates tables)
python init_db.py

# Seed database with sample data
python init_db.py --seed

# Run development server
python run.py
# Access at: http://127.0.0.1:5000
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api_events.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app
```

### Database Management

```bash
# Reset database (delete and recreate)
rm instance/marathon_registration.db
python init_db.py --seed
```

## Application Structure

- Entry point: `run.py`
- Configuration: `config.py`
- Database initialization: `init_db.py`
- Application factory pattern in `app/__init__.py`
