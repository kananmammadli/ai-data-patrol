import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import Base, engine
from app.models import User

def drop_tables():
    """Drop all database tables."""
    try:
        Base.metadata.drop_all(bind=engine)
        print("All tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        sys.exit(1)

def init_db():
    """Initialize the database by creating all tables."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        sys.exit(1)

def check_db_connection():
    """Check if the database connection is working."""
    try:
        # Try to connect to the database
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check database connection
    if not check_db_connection():
        print("Please ensure PostgreSQL is running and the database exists.")
        sys.exit(1)
    
    # Drop existing tables
    print("\nDropping existing tables...")
    drop_tables()
    
    # Initialize database
    print("\nCreating tables...")
    init_db()
    
    print("\nDatabase initialization completed successfully!") 