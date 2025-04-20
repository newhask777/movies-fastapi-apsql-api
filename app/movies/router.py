from fastapi import APIRouter, Depends
from app.movies.filters import MovieFilter
from app.movies.requests.requests import FilterArgsPy, MovieFilterRequest
from app.movies.service import MovieService
 

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/")
async def get_movies():
    return await MovieService.find_all()


@router.get("/limit")
async def get_movies(count: int):
    return await MovieService.get_limit_movies(count)


@router.get("/filter")
async def get_movies(limit: int, filters: FilterArgsPy = Depends()):
    filter_dict = filters.dict(exclude_none=True)
    return await MovieFilter.get_filtered_records(filter_dict, limit)


@router.get("/search")
async def get_movies_test(filters: MovieFilterRequest = Depends()):
    return await MovieFilter.get_filtered_movies(filters)

