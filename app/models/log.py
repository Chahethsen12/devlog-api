from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    language = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    mood = Column(String, nullable=True)
    tags = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="logs")