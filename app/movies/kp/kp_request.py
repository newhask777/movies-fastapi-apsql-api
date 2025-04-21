import pprint
import requests
import json
from kp_db import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from kp_models import Movie
from datetime import date, datetime
from datetime import datetime, date


db = SessionLocal() 


year = "2024"

for i in range(1, 23):

    print(i)

    url = f'https://api.kinopoisk.dev/v1.4/movie?page={i}&limit=250&selectFields=id&selectFields=externalId&selectFields=name&selectFields=enName&selectFields=alternativeName&selectFields=names&selectFields=description&selectFields=shortDescription&selectFields=slogan&selectFields=type&selectFields=typeNumber&selectFields=isSeries&selectFields=status&selectFields=year&selectFields=releaseYears&selectFields=rating&selectFields=ratingMpaa&selectFields=ageRating&selectFields=votes&selectFields=seasonsInfo&selectFields=budget&selectFields=audience&selectFields=movieLength&selectFields=seriesLength&selectFields=totalSeriesLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=backdrop&selectFields=logo&selectFields=ticketsOnSale&selectFields=videos&selectFields=networks&selectFields=persons&selectFields=facts&selectFields=fees&selectFields=premiere&selectFields=sequelsAndPrequels&selectFields=watchability&selectFields=lists&selectFields=top10&selectFields=top250&selectFields=updatedAt&selectFields=createdAt&type=movie&year={year}'

    headers = {
        "X-API-KEY": "2BXP44B-HS3460R-JK4BV1F-WX08GD5"
    }

    params = {

    }

    response = requests.get(url, headers=headers).json()
    

    for item in response["docs"]:
        
        # pprint.pprint(item)

        movie = Movie()

        movie.kp_id = item["id"]
        movie.name = item["name"]
        movie.alt_name = item["alternativeName"]
        movie.en_name = item["enName"]
        movie.type = item["type"]
        movie.type_number = item["typeNumber"]
        movie.year = item["year"]
        movie.description = item["description"]
        movie.short_description = item["shortDescription"]
        movie.status = item["status"]
        movie.rating = item["rating"]
        movie.votes = item["votes"]
        movie.movie_length = item["movieLength"]
        movie.age_rating = item["ageRating"]
        try:
            movie.poster = item["poster"]
        except:
            movie.poster = {}
        try:
            movie.genres = item["genres"]
        except:
            movie.genres = {}
        try:
            movie.countries = item["countries"]
        except:
            movie.countries = {}
        try:
            movie.persons = item["persons"]
        except:
            movie.persons = []
        try:
            movie.budget = item["budget"]
        except:
            movie.budget = {}
        try:
            movie.fees = item["fees"]
        except:
            movie.fees = {}
        try:
            movie.premier = item["premiere"]
        except:
            movie.premier = {}
        try:
            movie.seq_and_preq = item["sequelsAndPrequels"]
        except:
            movie.seq_and_preq = []
        try:
            movie.watchability = item["watchability"]
        except:
            movie.watchability = {}
        movie.top10 = item["top10"]
        movie.top250 = item["top250"]
        movie.tickets_on_sale = item["ticketsOnSale"] 
        movie.lists = item["lists"]


        db.add(movie)
        db.commit()





