from sqlalchemy import Column, String, Boolean
from app.db.base_class import Base

class GoogleOAuthConfig(Base):
    __tablename__ = "google_oauth_config"

    id = Column(String, primary_key=True, index=True)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    is_active = Column(Boolean, default=True) 