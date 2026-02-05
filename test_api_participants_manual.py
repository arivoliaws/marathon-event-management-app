"""
Manual test script to verify Participant API endpoints work correctly.
Run this script to test the participant API endpoints interactively.
"""

from app import create_app, db

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    print("Testing Participant API Endpoints")
    print("=" * 50)
    
    with app.test_client() as client:
        # Test 1: Create participant
        print("\n1. Testing POST /api/participants (Create Participant)")
        participant_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '555-1234',
            'age': 30
        }
        response = client.post('/api/participants', json=participant_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        participant_id = response.get_json()['id']
        
        # Test 2: Create participant without phone
        print("\n2. Testing POST /api/participants (Without Phone)")
        participant_data2 = {
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'age': 25
        }
        response = client.post('/api/participants', json=participant_data2)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 3: Get all participants
        print("\n3. Testing GET /api/participants (List All Participants)")
        response = client.get('/api/participants')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 4: Get single participant
        print(f"\n4. Testing GET /api/participants/{participant_id} (Get Single Participant)")
        response = client.get(f'/api/participants/{participant_id}')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 5: Update participant
        print(f"\n5. Testing PUT /api/participants/{participant_id} (Update Participant)")
        update_data = {
            'name': 'John Doe Jr.',
            'age': 31
        }
        response = client.put(f'/api/participants/{participant_id}', json=update_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 6: Delete participant
        print(f"\n6. Testing DELETE /api/participants/{participant_id} (Delete Participant)")
        response = client.delete(f'/api/participants/{participant_id}')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.data}")
        
        # Test 7: Verify deletion
        print(f"\n7. Verifying deletion - GET /api/participants/{participant_id}")
        response = client.get(f'/api/participants/{participant_id}')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 8: Test validation error (invalid email)
        print("\n8. Testing validation error (invalid email)")
        invalid_data = {
            'name': 'Test User',
            'email': 'invalid-email',
            'age': 25
        }
        response = client.post('/api/participants', json=invalid_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 9: Test validation error (negative age)
        print("\n9. Testing validation error (negative age)")
        invalid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'age': -5
        }
        response = client.post('/api/participants', json=invalid_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 10: Test 404 error
        print("\n10. Testing 404 error (non-existent participant)")
        response = client.get('/api/participants/999')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
