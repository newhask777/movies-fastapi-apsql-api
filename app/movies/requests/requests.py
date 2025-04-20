from typing import Any, Dict, List, Optional, Union
from sqlalchemy.ext.hybrid import hybrid_property

from fastapi import Query
from pydantic import BaseModel, Field, root_validator, validator

JSON = Union[Dict[str, 'JSON'], List['JSON'], str, int, float, bool, None]


class Rating(BaseModel):
    kp: float = 0.0
    imdb: float = 0.0
    filmCritics: float = 0.0
    russianFilmCritics: float = 0.0
    await_: float = 0.0  # Используем другое имя поля

    class Config:
        fields = {
            'await_': 'await'  # Маппинг для сериализации/десериализации
        }


class FilterArgsPy(BaseModel):

    kp_id: Optional[int] = None
    name: Union[str, None] = None
    alternativeName: Union[str, None] = None
    enName: Union[str, None] = None
    type: Union[str, None] = None
    typeNumber: Union[int, None] = None
    year: Union[int, None] = None
    description: Union[str, None] = None
    shortDescription: Union[str, None] = None
    status: Union[str, None] = None

    rating: Union[Rating] = None
    # votes: Optional[JSON] = None,

    # movieLength: Optional[int] = None,
    # ageRating: Optional[int] = None,

    # poster: Optional[JSON] = None,
    # genres: Optional[JSON] = None,
    # countries: Optional[JSON] = None,
    # persons: Optional[JSON] = None,
    # budget: Optional[JSON] = None,
    # fees: Optional[JSON] = None,
    # premier: Optional[JSON] = None,
    # seq_and_preq: Optional[JSON] = None,
    # watchability: Optional[JSON] = None,

    # top10: Optional[int] = None,
    # top250: Optional[int] = None,
    # tickets_on_sale: Optional[int] = None,
    # lists: Optional[list] = None,
   

    @root_validator(pre=True)
    def parse_nulls(cls, values: Dict[str, Any]):
        for field in ["name", "alternativeName", "enName", "type", "typeNumber", "rating"]:
            if values.get(field) == "null":
                values[field] = None
            
        return values
    

# Pydantic модель для фильтрации
class MovieFilterRequest(BaseModel):
    limit: int = Query(10, ge=1, le=100)
    rating_imdb: Optional[float] = Query(None, alias="rating.imdb")
    rating_kp: Optional[float] = Query(None, alias="rating.kp")
    status: Optional[str] = Query(None, alias="status")
    # Добавьте другие нужные поля

    class Config:
        allow_population_by_field_name = True