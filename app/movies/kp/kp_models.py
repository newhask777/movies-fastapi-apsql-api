from typing import Dict, Optional
from pydantic import BaseModel
from sqlalchemy import JSON, Boolean, Column, Date, ForeignKey, Integer, String, text
from kp_db import Base

class MetadataModel(BaseModel):
    poster: Optional[Dict[str, Optional[str]]] = {"path": None}

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
  
    kp_id = Column(Integer)
    name = Column(String, nullable=True)
    alternativeName = Column(String, nullable=True)
    enName = Column(String, nullable=True)
    type = Column(String, nullable=True)
    typeNumber = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    shortDescription = Column(String, nullable=True)
    status = Column(String, nullable=True)
    rating = Column(JSON, nullable=True)
    votes = Column(JSON, nullable=True)
    movieLength = Column(Integer, nullable=True)
    ageRating = Column(Integer, nullable=True)
    poster = Column(JSON, nullable=True)
    genres = Column(JSON, nullable=True)
    countries = Column(JSON, nullable=True)
    persons = Column(JSON, nullable=True)
    budget = Column(JSON, nullable=True)
    fees = Column(JSON, nullable=True)
    premier = Column(JSON, nullable=True)
    seq_and_preq = Column(JSON, nullable=True)
    watchability = Column(JSON, nullable=True)
    top10 = Column(Integer, nullable=True)
    top250 = Column(Integer, nullable=True)
    tickets_on_sale = Column(Boolean, nullable=True)
    lists = Column(JSON, nullable=True)
