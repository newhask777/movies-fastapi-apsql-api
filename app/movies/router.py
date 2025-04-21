from fastapi import APIRouter, Depends
from app.movies.filters import MovieFilter
from app.movies.requests.requests import MovieFilterRequest
from app.movies.service import MovieService
 

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/")
async def get_movies():
    return await MovieService.find_all()


@router.get("/search")
async def get_movies_test(filters: MovieFilterRequest = Depends()):
    return await MovieFilter.get_filtered_movies(filters)

