import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

def create_database():
    """Create the database if it doesn't exist."""
    load_dotenv()
    
    # Get database URL from environment
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/datapatrol")
    
    # Extract database name from URL
    db_name = db_url.split("/")[-1]
    
    # Create engine without database name
    base_url = "/".join(db_url.split("/")[:-1])
    engine = create_engine(f"{base_url}/postgres")
    
    try:
        # Check if database exists
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if not result.scalar():
                # Create database
                # Need to commit transaction before creating database
                conn.execute(text("COMMIT"))
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database '{db_name}' created successfully!")
            else:
                print(f"Database '{db_name}' already exists.")
    except OperationalError as e:
        print(f"Error creating database: {e}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    create_database() 