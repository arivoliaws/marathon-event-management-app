from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        # Import models here to ensure they are registered with SQLAlchemy
        from app import models
        
        # Create all database tables
        db.create_all()
    
    return app
