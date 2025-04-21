from typing import Dict
from sqlalchemy import cast, JSON
from sqlalchemy.sql.sqltypes import Float, String, Integer
from sqlalchemy.dialects.postgresql import JSONB

     
def build_filters(filter_params, model, filters):

    for field, value in vars(filter_params).items():
        if value is not None and hasattr(model, field):
            filters.append(getattr(model, field) == value)
    return filters


def build_json_filters(filter_params, model):
    rating_filters = []
    for param, value in vars(filter_params).items():
        if value is None:
            continue

        cast_type = Integer if isinstance(value, int) else \
                    Dict if isinstance(value, dict) else\
                    Float if isinstance(value, float) else \
                    String

        # Обработка специальных JSON-полей с массивами объектов
        if param == 'genres_name' or param == 'countries_name' and cast_type == String:
            model_field = param.split('_')[0]  # 'genres' или 'countries'
            json_key = param.split('_')[1]     # 'name'
            
            column = getattr(model, model_field, None)
            if column:
                rating_filters.append(
                    cast(column, JSONB).contains([{json_key: value}])
                )
            continue

        # Стандартная обработка JSON-полей
        parts = param.split('_')
        if len(parts) < 2:
            continue

        model_field, *json_keys = parts
        column = getattr(model, model_field, None)
        if not column:
            continue

        # Построение цепочки JSON-ключей
        json_access = column
        for key in json_keys:
            json_access = json_access[key]

        rating_filters.append(
            cast(json_access.astext, cast_type) == value
        )
    
    return rating_filters