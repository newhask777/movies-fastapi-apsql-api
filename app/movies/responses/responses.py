from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union


# Модель для элемента рейтинга (если нужна детализация)
class RatingResponse(BaseModel):
    kp: float
    imdb: float
    filmCritics: float
    russianFilmCritics: float
    await_: float = Field(alias="await")

# Модель для одного фильма
class MovieResponse(BaseModel):
    kp_id: int
    name: Optional[str]
    year: Optional[int] 
    status: Optional[str]
    alt_name: Optional[str]
    en_name: Optional[str]
    movie_type: Optional[str]
    type_number: Optional[int]
    year: Optional[int]
    description: Optional[str]
    short_description: Optional[str]
    rating: Optional[Dict[str, Any]] # или RatingResponse если используется структурированный рейтинг
    votes: Optional[Dict[str, Any]] 
    movie_length: Optional[int]
    age_rating: Optional[int]
    poster: Optional[Dict[str, Any]]
    genres: Optional[Union[Dict[str, Any], List[Any]]]
    countries: Optional[Union[Dict[str, Any], List[Any]]]
    persons: Optional[List[Dict]]
    budget: Optional[Dict[str, Any]]
    # fees: Optional[Dict[str, Any]]
    premier: Optional[Dict[str, Any]]
    seq_and_preq: Optional[List[Dict]]
    top10: Optional[int]
    top250: Optional[int]
    # lists: Optional[List[Any]]

    class Config:
        json_encoders = {
            dict: lambda v: v  # кастомная сериализация при необходимости
        }

# Модель для общего ответа
class MovieListResponse(BaseModel):
    results: List[MovieResponse]

