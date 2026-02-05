"""
Application entry point for the Marathon Registration Web Application.
Run this file to start the Flask development server.
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("Marathon Registration Web Application")
    print("="*60)
    print("\nStarting Flask development server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("\nAvailable pages:")
    print("  - Events:       http://127.0.0.1:5000/events")
    print("  - Participants: http://127.0.0.1:5000/participants")
    print("  - Invitations:  http://127.0.0.1:5000/invitations")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
