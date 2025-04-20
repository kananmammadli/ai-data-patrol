#!/usr/bin/env python3
"""
Database initialization script for DataPatrol.
This script creates the database and all necessary tables.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.init_db import init_db, check_db_connection, drop_tables
from app.db.create_db import create_database
from app.db.seed_db import seed_database

def main():
    """Main function to initialize the database."""
    print("Initializing DataPatrol database...")
    
    # Create database if it doesn't exist
    create_database()
    
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
    
    # Seed database with initial data
    print("\nSeeding database with initial data...")
    seed_database()
    
    print("\nDatabase initialization and seeding completed successfully!")

if __name__ == "__main__":
    main() 