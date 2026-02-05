"""
Manual test script to verify API endpoints work correctly.
Run this script to test the event API endpoints interactively.
"""

from app import create_app, db
from datetime import date, timedelta

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    print("Testing Event API Endpoints")
    print("=" * 50)
    
    with app.test_client() as client:
        # Test 1: Create event
        print("\n1. Testing POST /api/events (Create Event)")
        future_date = (date.today() + timedelta(days=30)).isoformat()
        event_data = {
            'name': 'Boston Marathon',
            'date': future_date,
            'location': 'Boston, MA',
            'distance': 42.195
        }
        response = client.post('/api/events', json=event_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        event_id = response.get_json()['id']
        
        # Test 2: Get all events
        print("\n2. Testing GET /api/events (List All Events)")
        response = client.get('/api/events')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 3: Get single event
        print(f"\n3. Testing GET /api/events/{event_id} (Get Single Event)")
        response = client.get(f'/api/events/{event_id}')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 4: Update event
        print(f"\n4. Testing PUT /api/events/{event_id} (Update Event)")
        update_data = {'name': 'Boston Marathon 2024'}
        response = client.put(f'/api/events/{event_id}', json=update_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 5: Delete event
        print(f"\n5. Testing DELETE /api/events/{event_id} (Delete Event)")
        response = client.delete(f'/api/events/{event_id}')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.data}")
        
        # Test 6: Verify deletion
        print(f"\n6. Verifying deletion - GET /api/events/{event_id}")
        response = client.get(f'/api/events/{event_id}')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 7: Test validation error
        print("\n7. Testing validation error (missing name)")
        invalid_data = {
            'name': '',
            'date': future_date,
            'location': 'Test',
            'distance': 10
        }
        response = client.post('/api/events', json=invalid_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 8: Test 404 error
        print("\n8. Testing 404 error (non-existent event)")
        response = client.get('/api/events/999')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
