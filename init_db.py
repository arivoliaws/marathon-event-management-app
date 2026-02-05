"""
Database initialization script for Marathon Registration Application.
Creates all tables and optionally seeds sample data for development.
"""

from datetime import datetime, timedelta
from app import create_app, db
from app.models import MarathonEvent, Participant, Invitation


def init_database(seed_data=False):
    """
    Initialize the database by creating all tables.
    
    Args:
        seed_data (bool): If True, populate database with sample data for development
    """
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        if seed_data:
            seed_sample_data()
            print("✓ Sample data seeded successfully")


def seed_sample_data():
    """
    Seed the database with sample data for development and testing.
    """
    # Clear existing data
    db.session.query(Invitation).delete()
    db.session.query(Participant).delete()
    db.session.query(MarathonEvent).delete()
    db.session.commit()
    
    # Create sample marathon events
    events = [
        MarathonEvent(
            name="Boston Marathon 2026",
            date=datetime(2026, 4, 20).date(),
            location="Boston, MA",
            distance=42.195
        ),
        MarathonEvent(
            name="New York City Marathon 2026",
            date=datetime(2026, 11, 1).date(),
            location="New York, NY",
            distance=42.195
        ),
        MarathonEvent(
            name="Chicago Half Marathon 2026",
            date=datetime(2026, 9, 27).date(),
            location="Chicago, IL",
            distance=21.0975
        ),
        MarathonEvent(
            name="San Francisco 10K 2026",
            date=datetime(2026, 7, 4).date(),
            location="San Francisco, CA",
            distance=10.0
        )
    ]
    
    for event in events:
        db.session.add(event)
    db.session.commit()
    
    # Create sample participants
    participants = [
        Participant(
            name="Alice Johnson",
            email="alice.johnson@example.com",
            phone="555-0101",
            age=28
        ),
        Participant(
            name="Bob Smith",
            email="bob.smith@example.com",
            phone="555-0102",
            age=35
        ),
        Participant(
            name="Carol Williams",
            email="carol.williams@example.com",
            phone="555-0103",
            age=42
        ),
        Participant(
            name="David Brown",
            email="david.brown@example.com",
            phone="555-0104",
            age=31
        ),
        Participant(
            name="Emma Davis",
            email="emma.davis@example.com",
            phone=None,
            age=26
        )
    ]
    
    for participant in participants:
        db.session.add(participant)
    db.session.commit()
    
    # Create sample invitations
    invitations = [
        Invitation(participant_id=1, event_id=1),  # Alice -> Boston Marathon
        Invitation(participant_id=1, event_id=3),  # Alice -> Chicago Half Marathon
        Invitation(participant_id=2, event_id=1),  # Bob -> Boston Marathon
        Invitation(participant_id=2, event_id=2),  # Bob -> NYC Marathon
        Invitation(participant_id=3, event_id=2),  # Carol -> NYC Marathon
        Invitation(participant_id=4, event_id=3),  # David -> Chicago Half Marathon
        Invitation(participant_id=4, event_id=4),  # David -> SF 10K
        Invitation(participant_id=5, event_id=4),  # Emma -> SF 10K
    ]
    
    for invitation in invitations:
        db.session.add(invitation)
    db.session.commit()
    
    print(f"  - Created {len(events)} marathon events")
    print(f"  - Created {len(participants)} participants")
    print(f"  - Created {len(invitations)} invitations")


if __name__ == '__main__':
    import sys
    
    # Check if --seed flag is provided
    seed = '--seed' in sys.argv
    
    print("Initializing Marathon Registration Database...")
    init_database(seed_data=seed)
    print("\nDatabase initialization complete!")
    
    if not seed:
        print("\nTip: Run with --seed flag to populate sample data for development:")
        print("  python init_db.py --seed")
