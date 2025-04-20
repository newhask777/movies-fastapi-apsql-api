from sqlalchemy import select
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.movies.models.data_models import Movie


class MovieService(BaseDAO): # Data access object or service or repo
    model = Movie

    @classmethod
    async def get_limit_movies(cls, limit: int):
        async with async_session_maker() as session:
            query = select(Movie).filter_by().limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
        
  

        
      