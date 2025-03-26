from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)


    app.db = connect_db(Config.DB_URI)
    from .routes import main

    app.register_blueprint(main)
    
    return app

def connect_db(db_uri):
    """
    Establish a direct connection to the PostgreSQL database using psycopg2.
    """
    try:
        conn = psycopg2.connect(db_uri)
        return conn
    except Exception as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None