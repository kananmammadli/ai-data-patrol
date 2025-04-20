import os
import sys
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from passlib.context import CryptContext

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import User, DBConnection, DataCheck, SeverityRecipient, UserRole, AuthProvider

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def seed_database():
    """Seed the database with initial data."""
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@datapatrol.io").first()
        if not admin_user:
            # Create admin user with password
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # In production, use a secure password
            admin_user = User(
                email="admin@datapatrol.io",
                role=UserRole.ADMIN,
                auth_provider=AuthProvider.PASSWORD,
                hashed_password=get_password_hash(admin_password),
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.flush()  # Flush to get the ID
            print("Created admin user")

        # Add a sample database connection
        sample_db = db.query(DBConnection).filter(DBConnection.name == "Sample PostgreSQL").first()
        if not sample_db:
            sample_db = DBConnection(
                name="Sample PostgreSQL",
                host="localhost",
                port=5432,
                database="sample_db",
                username="sample_user",
                encrypted_password="encrypted_password_placeholder"  # In production, this should be properly encrypted
            )
            db.add(sample_db)
            db.flush()  # Flush to get the ID
            print("Created sample database connection")

            # Add a sample data check
            sample_check = DataCheck(
                name="Sample Data Quality Check",
                organization="DataPatrol",
                project="Data Quality",
                description="Check for data quality issues in sample table",
                troubleshooting_guide="""
                If this check fails:
                1. Verify the sample table exists
                2. Check for missing or invalid data
                3. Contact data team if issues persist
                """,
                sql_script="""
                SELECT 
                    'Data Quality Issue' as issue_type,
                    COUNT(*) as issue_count,
                    3 as severity
                FROM sample_table
                WHERE quality_score < 0.8
                """,
                schedule="0 9 * * *",  # Run at 9 AM daily
                expiry_period_hours=24,
                max_attachment_rows=100,
                db_connection=sample_db  # Set the relationship
            )
            db.add(sample_check)
            db.flush()  # Flush to get the ID
            print("Created sample data check")

            # Add severity recipients for the sample check
            severity_recipient = SeverityRecipient(
                data_check=sample_check,  # Set the relationship
                min_severity=2,
                max_severity=5,
                emails="alerts@datapatrol.io,oncall@datapatrol.io"
            )
            db.add(severity_recipient)
            print("Created sample severity recipient")

        # Commit all changes
        db.commit()
        print("Database seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    load_dotenv()
    seed_database() 