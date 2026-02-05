# Product Overview

Marathon Registration Web Application - a Flask-based system for managing marathon events, participant registries, and event invitations.

## Purpose

Enables administrators to:
- Create and manage marathon events across multiple locations
- Maintain a participant registry with contact information
- Send event invitations linking participants to specific events
- Access data through both web interface and REST APIs

## Key Features

- Real-time database persistence (SQLite)
- RESTful API with JSON responses
- HTML web interface for browser-based management
- Comprehensive data validation
- Cascade deletion for referential integrity
- Support for filtering invitations by event or participant

## User Roles

- **Administrator**: Primary user who manages events, participants, and invitations through web UI or API
- **Developer/External System**: Can interact programmatically via REST API endpoints
