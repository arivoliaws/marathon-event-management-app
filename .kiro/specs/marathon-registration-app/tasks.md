# Implementation Plan: Marathon Registration Web Application

## Overview

This implementation plan breaks down the Flask-based Marathon Registration Web Application into discrete coding tasks. The application will be built incrementally, starting with the data layer, then the API layer, followed by the web interface, and finally comprehensive testing. Each task builds on previous work to ensure a cohesive, working application.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create Flask application directory structure (app/, tests/, templates/, static/)
  - Create requirements.txt with Flask, SQLAlchemy, Hypothesis, pytest, WTForms
  - Create app/__init__.py to initialize Flask app and SQLAlchemy
  - Create config.py for application configuration (database URI, secret key)
  - _Requirements: 4.1, 4.2, 4.3, 6.1, 6.2, 6.3_

- [ ] 2. Implement database models
  - [ ] 2.1 Create SQLAlchemy models for MarathonEvent, Participant, and Invitation
    - Define MarathonEvent model with id, name, date, location, distance, timestamps
    - Define Participant model with id, name, email, phone, age, timestamps
    - Define Invitation model with id, participant_id, event_id, sent_at, and relationships
    - Configure foreign key constraints and cascade deletions
    - _Requirements: 1.1, 2.1, 3.1, 7.3_

  - [ ]* 2.2 Write property test for model creation and retrieval
    - **Property 1: Create operation persistence**
    - **Validates: Requirements 1.1, 2.1, 3.1, 5.1**

  - [ ] 2.3 Create database initialization script
    - Write function to create all tables
    - Add sample data seeding for development
    - _Requirements: 5.1_

- [ ] 3. Implement validation functions
  - [ ] 3.1 Create validation module with event, participant, and invitation validators
    - Implement validate_event() checking name, date, location, distance
    - Implement validate_participant() checking name, email format, age
    - Implement validate_invitation() checking participant and event existence
    - Return (is_valid, errors) tuple with field-specific error messages
    - _Requirements: 1.5, 2.5, 7.1, 7.2, 7.3, 7.4_

  - [ ]* 3.2 Write property test for event validation
    - **Property 7: Event validation correctness**
    - **Validates: Requirements 1.5, 7.1**

  - [ ]* 3.3 Write property test for participant validation
    - **Property 8: Participant validation correctness**
    - **Validates: Requirements 2.5, 7.2**

  - [ ]* 3.4 Write property test for invitation validation
    - **Property 9: Invitation referential integrity**
    - **Validates: Requirements 7.3**

  - [ ]* 3.5 Write unit tests for validation edge cases
    - Test empty strings, whitespace-only strings
    - Test boundary values (age=0, age=1, distance=0.0, distance=0.1)
    - Test various invalid email formats
    - Test past dates, current date, future dates
    - _Requirements: 7.1, 7.2, 7.3_

- [ ] 4. Implement REST API for marathon events
  - [ ] 4.1 Create API blueprint and event CRUD endpoints
    - Implement POST /api/events (create event with validation)
    - Implement GET /api/events (list all events)
    - Implement GET /api/events/<id> (get single event)
    - Implement PUT /api/events/<id> (update event with validation)
    - Implement DELETE /api/events/<id> (delete event)
    - Add proper error handling with rollback on failures
    - Return appropriate HTTP status codes (200, 201, 204, 400, 404, 500)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 4.1, 4.4, 4.5, 4.6, 5.1, 5.4_

  - [ ]* 4.2 Write property test for event CRUD operations
    - **Property 1: Create operation persistence** (events)
    - **Property 2: Read all operation completeness** (events)
    - **Property 3: Update operation persistence** (events)
    - **Property 4: Delete operation removal** (events)
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 5.1**

  - [ ]* 4.3 Write property test for event API HTTP status codes
    - **Property 10: Successful operation status codes** (events)
    - **Property 11: Invalid input status codes** (events)
    - **Property 12: Non-existent resource status codes** (events)
    - **Validates: Requirements 4.4, 4.5, 4.6**

  - [ ]* 4.4 Write unit tests for event API edge cases
    - Test creating event with missing fields
    - Test updating non-existent event
    - Test deleting non-existent event
    - _Requirements: 1.5, 4.5, 4.6_

- [ ] 5. Implement REST API for participants
  - [ ] 5.1 Create participant CRUD endpoints
    - Implement POST /api/participants (create participant with validation)
    - Implement GET /api/participants (list all participants)
    - Implement GET /api/participants/<id> (get single participant)
    - Implement PUT /api/participants/<id> (update participant with validation)
    - Implement DELETE /api/participants/<id> (delete participant)
    - Add proper error handling with rollback on failures
    - Return appropriate HTTP status codes
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 4.2, 4.4, 4.5, 4.6, 5.1, 5.4_

  - [ ]* 5.2 Write property test for participant CRUD operations
    - **Property 1: Create operation persistence** (participants)
    - **Property 2: Read all operation completeness** (participants)
    - **Property 3: Update operation persistence** (participants)
    - **Property 4: Delete operation removal** (participants)
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 5.1**

  - [ ]* 5.3 Write property test for participant API HTTP status codes
    - **Property 10: Successful operation status codes** (participants)
    - **Property 11: Invalid input status codes** (participants)
    - **Property 12: Non-existent resource status codes** (participants)
    - **Validates: Requirements 4.4, 4.5, 4.6**

  - [ ]* 5.4 Write unit tests for participant API edge cases
    - Test duplicate email registration
    - Test invalid email formats
    - Test negative age values
    - _Requirements: 2.5, 4.5_

- [ ] 6. Implement REST API for invitations
  - [ ] 6.1 Create invitation CRUD endpoints
    - Implement POST /api/invitations (create invitation with validation)
    - Implement GET /api/invitations (list all invitations with nested participant/event data)
    - Implement GET /api/invitations?event_id=<id> (filter by event)
    - Implement GET /api/invitations?participant_id=<id> (filter by participant)
    - Implement DELETE /api/invitations/<id> (delete invitation)
    - Add proper error handling with rollback on failures
    - Return appropriate HTTP status codes
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.3, 4.4, 4.5, 4.6, 5.1, 5.4_

  - [ ]* 6.2 Write property test for invitation CRUD operations
    - **Property 1: Create operation persistence** (invitations)
    - **Property 2: Read all operation completeness** (invitations)
    - **Property 4: Delete operation removal** (invitations)
    - **Validates: Requirements 3.1, 3.2, 3.5, 5.1**

  - [ ]* 6.3 Write property test for invitation filtering
    - **Property 5: Event-based invitation filtering**
    - **Property 6: Participant-based invitation filtering**
    - **Validates: Requirements 3.3, 3.4**

  - [ ]* 6.4 Write unit tests for invitation referential integrity
    - Test creating invitation with non-existent participant
    - Test creating invitation with non-existent event
    - Test cascade deletion (delete event, verify invitations removed)
    - _Requirements: 7.3_

- [ ] 7. Checkpoint - Ensure all API tests pass
  - Run all tests to verify API functionality
  - Ensure all tests pass, ask the user if questions arise

- [ ] 8. Implement web interface for events
  - [ ] 8.1 Create event management templates and routes
    - Create templates/events.html with event list, create form, edit forms, delete buttons
    - Implement GET /events route to display all events
    - Implement POST /events/create route to handle event creation
    - Implement POST /events/<id>/update route to handle event updates
    - Implement POST /events/<id>/delete route to handle event deletion
    - Add JavaScript for AJAX updates (create/update/delete without page refresh)
    - Display validation errors in the UI
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 5.2, 6.1, 6.4, 6.5_

  - [ ]* 8.2 Write unit tests for event web routes
    - Test GET /events returns correct template with data
    - Test POST /events/create with valid and invalid data
    - Test form validation error display
    - _Requirements: 6.1, 6.5_

- [ ] 9. Implement web interface for participants
  - [ ] 9.1 Create participant management templates and routes
    - Create templates/participants.html with participant list, create form, edit forms, delete buttons
    - Implement GET /participants route to display all participants
    - Implement POST /participants/create route to handle participant creation
    - Implement POST /participants/<id>/update route to handle participant updates
    - Implement POST /participants/<id>/delete route to handle participant deletion
    - Add JavaScript for AJAX updates
    - Display validation errors in the UI
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 5.2, 6.2, 6.4, 6.5_

  - [ ]* 9.2 Write unit tests for participant web routes
    - Test GET /participants returns correct template with data
    - Test POST /participants/create with valid and invalid data
    - Test form validation error display
    - _Requirements: 6.2, 6.5_

- [ ] 10. Implement web interface for invitations
  - [ ] 10.1 Create invitation management templates and routes
    - Create templates/invitations.html with invitation list, create form, delete buttons
    - Display participant and event details for each invitation
    - Implement GET /invitations route to display all invitations
    - Implement POST /invitations/create route to handle invitation creation
    - Implement POST /invitations/<id>/delete route to handle invitation deletion
    - Add dropdowns populated with existing participants and events
    - Add JavaScript for AJAX updates
    - Display validation errors in the UI
    - _Requirements: 3.1, 3.2, 3.5, 5.2, 6.3, 6.4, 6.5_

  - [ ]* 10.2 Write unit tests for invitation web routes
    - Test GET /invitations returns correct template with data
    - Test POST /invitations/create with valid and invalid references
    - _Requirements: 6.3, 6.5_

- [ ] 11. Create base template and styling
  - [ ] 11.1 Create base layout and navigation
    - Create templates/base.html with navigation menu
    - Add links to Events, Participants, and Invitations pages
    - Create static/style.css with basic styling
    - Ensure responsive design for mobile and desktop
    - _Requirements: 6.1, 6.2, 6.3_

- [ ] 12. Implement transaction rollback property test
  - [ ]* 12.1 Write property test for transaction rollback
    - **Property 13: Transaction rollback on failure**
    - Simulate database failures and verify rollback behavior
    - **Validates: Requirements 5.4**

- [ ] 13. Create application entry point and configuration
  - [ ] 13.1 Create main application runner
    - Create run.py or app.py as entry point
    - Configure Flask app with database URI and secret key
    - Initialize database on first run
    - Add development server configuration
    - _Requirements: 5.1, 5.2_

  - [ ]* 13.2 Write integration tests for complete workflows
    - Test: create event → create participant → send invitation → verify all exist
    - Test: delete event → verify invitations are cascade deleted
    - Test: refresh page → verify data persists without restart
    - _Requirements: 5.2, 7.3_

- [ ] 14. Final checkpoint - Ensure all tests pass
  - Run complete test suite (unit tests and property tests)
  - Verify web interface works correctly in browser
  - Test real-time updates without page refresh
  - Ensure all tests pass, ask the user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples and edge cases
- The implementation follows a bottom-up approach: models → validation → API → web interface
- AJAX functionality ensures real-time updates without page refresh
- All database operations use immediate commits with rollback on errors
