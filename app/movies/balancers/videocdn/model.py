from sqlalchemy import Boolean, Column, Integer, String
from db import Base
from sqlalchemy.dialects.postgresql import JSONB


class MovieVCDN(Base):
    __tablename__ = "videocdn"

    id = Column(Integer, primary_key=True)
    
    videocdn_id = Column(Integer, nullable=True)
    ru_title = Column(String, nullable=True)
    orig_title = Column(String, nullable=True)
    imdb_id = Column(String, nullable=True)
    kinopoisk_id = Column(Integer, nullable=True)
    created = Column(String, nullable=True)
    released = Column(String, nullable=True)
    updated = Column(String, nullable=True)
    iframe_src = Column(String, nullable=True)
    iframe = Column(String, nullable=True)
    poster = Column(JSONB, nullable=True)
    year = Column(String, nullable=True)
    content_type = Column(String, nullable=True)
    media = Column(JSONB, nullable=True)
    translations = Column(JSONB, nullable=True)
    default_media_id = Column(Integer, nullable=True)

