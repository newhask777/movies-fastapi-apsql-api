from typing import Any, Dict, Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import JSONB


@dataclass
class Movie(Base):
    __tablename__ = 'movies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    kp_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String, nullable=True)
    alternativeName: Mapped[str] = mapped_column(String, nullable=True)
    enName: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[String] = mapped_column(String, nullable=True)
    typeNumber: Mapped[int] = mapped_column(Integer, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    shortDescription: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    votes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    movieLength: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    ageRating: Mapped[int] = mapped_column(Integer, nullable=True)
    poster: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    genres: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    countries: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    persons: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    budget: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    fees: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    premier: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    seq_and_preq: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    watchability: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    top10: Mapped[int] = mapped_column(Integer, nullable=False)
    top250: Mapped[int] = mapped_column(Integer, nullable=False)
    tickets_on_sale: Mapped[bool] = mapped_column(Boolean, nullable=False)
    lists: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)