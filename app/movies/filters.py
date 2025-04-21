from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import select, and_, cast
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Float as SQLFloat

from app.database import async_session_maker
from app.movies.helpers.filters import build_filters, build_json_filters
from app.movies.models.data_models import Movie
from app.movies.responses.responses import MovieListResponse, MovieResponse


class MovieFilter:
     
    @classmethod
    async def get_filtered_movies(cls, filter_params: dict):
        async with async_session_maker() as session:
            try:
                query = select(Movie)
                

                filters = []
                json_filters = []

                json_filters = build_json_filters(filter_params, Movie)

                filters = build_filters(filter_params, Movie, filters)
                
                
                if json_filters:
                    filters.append(and_(*json_filters))
    
                if filters:
                    query = query.where(and_(*filters))
                

                query = query.limit(filter_params.limit)
                

                result = await session.execute(query)
                movies = result.scalars().all()
                

                return MovieListResponse(
                    results=[
                        MovieResponse(
                            kp_id=movie.kp_id,
                            name=movie.name,
                            alt_name=movie.alt_name,
                            en_name=movie.en_name,
                            movie_type=movie.type,
                            type_number=movie.type_number,
                            description=movie.description,
                            short_description=movie.short_description,
                            year=movie.year,
                            status=movie.status,
                            rating=movie.rating,
                            votes=movie.votes,
                            movie_length=movie.movie_length,
                            age_rating=movie.age_rating,
                            poster=movie.poster,
                            genres=movie.genres,
                            countries=movie.countries,
                            persons=movie.persons,
                            budget=movie.budget,
                            # fees=movie.fees,
                            premier=movie.premier,
                            seq_and_preq=movie.seq_and_preq,
                            top10=movie.top10,
                            top250=movie.top250,
                            # lists=movie.lists
                        )
                        for movie in movies
                    ]
                )

            
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
                



        