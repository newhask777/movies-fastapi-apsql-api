from datetime import date
from fastapi import FastAPI, Query, Depends
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/predictions')
def get_today_predictions():
    return "sdf"

class HotelSearchArgs:
    def __init__(
            self,
            date_from: date, 
            date_to: date, 
            location: str, 
            stars: Optional[int] = Query(None, qe=1, le=5), 
            has_spa: Optional[bool] = None
            ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars =stars
        self.has_spa = has_spa
        

@app.get('/hotels')
# @app.get('/hotels', response_model=list[SHotels])
def get_hotels(search_args: HotelSearchArgs = Depends()):

    hotels = [
        {
            "address": "ul.Gagarina, 1, Altay",
            "name": "Super Hotel",
            "stars": 5,
        }
    ]
    return hotels

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post('/bookings')
def add_booking(booking: SBooking):
    pass
