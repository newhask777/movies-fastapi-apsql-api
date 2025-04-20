from datetime import date
from fastapi import FastAPI, Query, Depends
from typing import List, Optional
from pydantic import BaseModel
from app.movies.router import router as router_movies

app = FastAPI()

app.include_router(router_movies)





