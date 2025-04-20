from sqlalchemy import Boolean, Column, Integer, String, text
from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB

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
    rating = Column(JSONB, nullable=True)
    votes = Column(JSONB, nullable=True)
    movieLength = Column(Integer, nullable=True)
    ageRating = Column(Integer, nullable=True)
    poster = Column(JSONB, nullable=True)
    genres = Column(JSONB, nullable=True)
    countries = Column(JSONB, nullable=True)
    persons = Column(JSONB, nullable=True)
    budget = Column(JSONB, nullable=True)
    fees = Column(JSONB, nullable=True)
    premier = Column(JSONB, nullable=True)
    seq_and_preq = Column(JSONB, nullable=True)
    watchability = Column(JSONB, nullable=True)
    top10 = Column(Integer, nullable=True)
    top250 = Column(Integer, nullable=True)
    tickets_on_sale = Column(Boolean, nullable=True)
    lists = Column(JSONB, nullable=True)

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.kp_id}', year={self.year})>"


