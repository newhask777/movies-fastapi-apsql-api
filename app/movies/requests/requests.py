from typing import Any, Dict, List, Optional, Union
from sqlalchemy.ext.hybrid import hybrid_property

from fastapi import Query
from pydantic import BaseModel, validator


# Pydantic модель для фильтрации
class MovieFilterRequest(BaseModel):
    limit: int = Query(10, ge=1, le=251)

    kp_id: Optional[int] = Query(None, alias="kp_id")
    name: Optional[str] = Query(None, alias="name")
    alt_name: Optional[str] = Query(None, alias="alt_name")
    en_name: Optional[str] = Query(None, alias="en_name")
    type: Optional[str] = Query(None, alias="movie_type")
    type_number: Optional[int] = Query(None, alias="type_number")
    year: Optional[int] = Query(None, alias="year")
    description: Optional[str] = Query(None, alias="description")
    short_description: Optional[str] = Query(None, alias="short_description")
    status: Optional[str] = Query(None, alias="status")
    # json
    rating_imdb: Optional[float] = Query(None, alias="rating.imdb")
    rating_kp: Optional[float] = Query(None, alias="rating.kp")
    votes_kp: Optional[float] = Query(None, alias="votes.kp")
    votes_imdb: Optional[float] = Query(None, alias="votes.imdb")

    movie_length: Optional[int] = Query(None, alias="movie_length")
    age_rating: Optional[int] = Query(None, alias="age_rating")
    # json
    poster_url: Optional[str] = Query(None, alias="rating.url")
    poster_preview_url: Optional[str] = Query(None, alias="rating.previewUrl")
    genres_name: Optional[str] = Query(None, alias="genres.name")
    countries_name: Optional[str] = Query(None, alias="countries.name")
    persons: Optional[str] = Query(None, alias="persons")
    budget_currency: Optional[str] = Query(None, alias="budget.currency")
    budget_value: Optional[int] = Query(None, alias="budget.value")
    # fees_world_value: Optional[str] = Query(None, alias="fees.world.value")
    premiere_world: Optional[str] = Query(None, alias="premier.world")
    seq_and_preq: Optional[str] = Query(None, alias="sequelsAndPrequels")
    top10: Optional[int] = Query(None, alias="top10")
    top250: Optional[int] = Query(None, alias="top250")
    # lists: Optional[str] = Query(None, alias="lists")
   

    class Config:
        allow_population_by_field_name = True