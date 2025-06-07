from typing import Any, Dict, List, Optional
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
    alt_name: Mapped[str] = mapped_column(String, nullable=True)
    en_name: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[String] = mapped_column(String, nullable=True)
    type_number: Mapped[int] = mapped_column(Integer, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    short_description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    votes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    movie_length: Mapped[int] = mapped_column(Integer, nullable=True)
    age_rating: Mapped[int] = mapped_column(Integer, nullable=True)
    poster: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    genres: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    countries: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    persons: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    budget: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    fees: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    premier: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    seq_and_preq: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    watchability: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    top10: Mapped[int] = mapped_column(Integer, nullable=True)
    top250: Mapped[int] = mapped_column(Integer, nullable=True)
    tickets_on_sale: Mapped[bool] = mapped_column(Boolean, nullable=True)
    lists: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)



@dataclass
class MovieVCDN(Base):
    __tablename__ = 'videocdn'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    videocdn_id: Mapped[str] = mapped_column(String, nullable=True)
    ru_title: Mapped[str] = mapped_column(String, nullable=True)
    orig_title: Mapped[str] = mapped_column(String, nullable=True)
    imdb_id: Mapped[str] = mapped_column(String, nullable=True)
    kinopoisk_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created: Mapped[str] = mapped_column(String, nullable=True)
    released: Mapped[str] = mapped_column(String, nullable=True)
    updated: Mapped[str] = mapped_column(String, nullable=True)
    iframe_src: Mapped[str] = mapped_column(String, nullable=True)
    iframe: Mapped[str] = mapped_column(String, nullable=True)
    year: Mapped[str] = mapped_column(String, nullable=True)
    content_type: Mapped[str] = mapped_column(String, nullable=True)
    media: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    translations: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    default_media_id: Mapped[str] = mapped_column(String, nullable=True)