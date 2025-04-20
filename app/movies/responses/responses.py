from pydantic import BaseModel, Field
from typing import List, Dict, Any


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
    name: str
    year: int
    status: str
    rating: Dict[str, Any]  # или RatingResponse если используется структурированный рейтинг

    class Config:
        json_encoders = {
            dict: lambda v: v  # кастомная сериализация при необходимости
        }

# Модель для общего ответа
class MovieListResponse(BaseModel):
    results: List[MovieResponse]

