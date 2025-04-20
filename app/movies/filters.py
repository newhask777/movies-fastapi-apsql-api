from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import select, and_, cast
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Float as SQLFloat

from app.database import async_session_maker
from app.movies.models.data_models import Movie
from app.movies.responses.responses import MovieListResponse, MovieResponse


class MovieFilter:
     
    @classmethod
    async def get_filtered_movies(cls, filter_params: dict):
        async with async_session_maker() as session:
            try:
                query = select(Movie)
                
                # Собираем условия фильтрации
                filters = []
                
                # Обрабатываем рейтинг
                rating_filters = []
                if filter_params.rating_imdb is not None:
                    rating_filters.append(
                        cast(Movie.rating['imdb'].astext, SQLFloat) == filter_params.rating_imdb
                    )
                if filter_params.rating_kp is not None:
                    rating_filters.append(
                        cast(Movie.rating['kp'].astext, SQLFloat) == filter_params.rating_kp
                    )
                
                if filter_params.status is not None:
                    rating_filters.append(
                        Movie.status == filter_params.status
                    )
                
                if rating_filters:
                    filters.append(and_(*rating_filters))
                
                # Применяем фильтры
                if filters:
                    query = query.where(and_(*filters))
                
                # Добавляем лимит
                query = query.limit(filter_params.limit)
                
                # Выполняем запрос
                result = await session.execute(query)
                movies = result.scalars().all()
                

                return MovieListResponse(
                    results=[
                        MovieResponse(
                            kp_id=movie.kp_id,
                            name=movie.name,
                            year=movie.year,
                            status=movie.status,
                            rating=movie.rating
                        )
                        for movie in movies
                    ]
                )

            
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
                



        