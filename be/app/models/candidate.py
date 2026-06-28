from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    experience_years = Column(Float, default=0.0)
    education = Column(String)
    skills = Column(JSON) # Store list of skills
    raw_text = Column(Text) # Full extracted text
