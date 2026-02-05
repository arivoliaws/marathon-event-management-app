from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    # Get the path to the project root (parent of app directory)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(basedir, 'templates')
    static_dir = os.path.join(basedir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        # Import models here to ensure they are registered with SQLAlchemy
        from app import models
        
        # Create all database tables
        db.create_all()
    
    # Register API blueprint
    from app.api import api
    app.register_blueprint(api)
    
    # Register web routes blueprint
    from app.web_routes import web
    app.register_blueprint(web)
    
    return app
