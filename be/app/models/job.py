from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    required_skills = Column(JSON)
    experience_level = Column(Float, default=0.0)
