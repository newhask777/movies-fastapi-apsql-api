import asyncio
import json
import httpx
from sqlalchemy.orm import Session
from tqdm import tqdm
from service import save_movie_to_db
from db import SessionLocal
from model import Movie

# Конфигурация
BATCH_SIZE = 10

kp_tokens = [
    # "2BXP44B-HS3460R-JK4BV1F-WX08GD5", # exp newhaskellisp 
    # "5PV2AF3-NC1M1R8-MMXYPP6-HY7NN2X",# haskellisp
    # "RJFHMJ6-NCMMB18-Q9909GP-D8R7AGR", # ivanhask369
    # "GDK9FDJ-Y7V4096-N4XFK29-9EX38VQ", # barakdimon  
    # "TSG399W-WJ7MSTM-NET4M6F-6EN5ZBA", # lehazarutel 
    # "4NAC79D-8YY4WEJ-MGTBHM1-AF3WMR4" # hanzfierman 
    # "A287HMK-ZKTMKHR-MFJQNJ8-FC6YPJS" # petermuller 
    #"47F41BE-90GMH6S-H0A4HNH-0TTWJPA" # marekkovalskiy
    # "NZPGQMX-05S4K52-KCMZT70-SMZ5K40" # retrodrop
    "02NCAWE-TJM493H-GZP1DWM-9B5J7HJ" # some one
]

VIDEOCDN_API_KEY = "lTf8tBnZLmO0nHTyRaSlvGI5UH1ddZ2f"
VIDEOSEED_TOKEN = "d503c3e71a5c120705c9c591ef734119"

db = SessionLocal()

async def fetch_kinopoisk_movies(session: httpx.AsyncClient, page: int, year: int):

    for token in kp_tokens:
        print(year)
        
        url = f'https://api.kinopoisk.dev/v1.4/movie?page={page}&limit=250&selectFields=id&selectFields=externalId&selectFields=name&selectFields=enName&selectFields=alternativeName&selectFields=names&selectFields=description&selectFields=shortDescription&selectFields=type&selectFields=typeNumber&selectFields=isSeries&selectFields=status&selectFields=year&selectFields=releaseYears&selectFields=rating&selectFields=ageRating&selectFields=votes&selectFields=budget&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&selectFields=fees&selectFields=premiere&selectFields=sequelsAndPrequels&selectFields=watchability&selectFields=lists&selectFields=top10&selectFields=updatedAt&type=movie&year={year}&selectFields=top250'
        
        headers = {"X-API-KEY": token}
        
        # url = "https://api.kinopoisk.dev/v1.4/movie"

        params = {
            "page": page,
            "limit": 250,
            "year": year,
            "type": "movie",
            "selectFields": ",".join([
                "id", "externalId", "name", "enName", "alternativeName", "names",
                "description", "shortDescription", "slogan", "type", "typeNumber",
                "isSeries", "status", "year", "releaseYears", "rating", "ratingMpaa",
                "ageRating", "votes", "seasonsInfo", "budget", "audience", "movieLength",
                "seriesLength", "totalSeriesLength", "genres", "countries", "poster",
                "backdrop", "logo", "ticketsOnSale", "videos", "networks", "persons",
                "facts", "fees", "premiere", "sequelsAndPrequels", "watchability",
                "lists", "top10", "top250", "updatedAt", "createdAt"
            ])
        }
        
        try:
            response = await session.get(url, headers=headers)
            # print(response.json())
            response.raise_for_status()

            print(page)

            return response.json().get("docs", [])
        except Exception as e:
            print(f"Kinopoisk error (page {page}): {str(e)}")
            return []


async def check_video_services(session: httpx.AsyncClient, kp_id: int):
    try:
        videocdn_url = f"https://portal.lumex.host/api/short?api_token={VIDEOCDN_API_KEY}&kinopoisk_id={kp_id}"

        videocdn_res = await asyncio.gather(
            session.get(videocdn_url)
        )

        # vdcdn_response = videocdn_res[0].json()  # Первый (и единственный) ответ
        
        # try:
        #     print(vdcdn_response)
        #     # print(vdseed_response)
                      
        # except Exception as e:
        #     print(f"Ошибка декодирования JSON: {e}")
           
        if(videocdn_res[0].json()['result'] != False):
            print(True)
            return True
        
    except Exception as e:
        print(f"Video services check error (ID {kp_id}): {str(e)}")
        return {"exists_in_videocdn": False, "exists_in_videoseed": False}


async def save_movie(session: httpx.AsyncClient, movie: dict, pbar: tqdm):
    kp_id = movie["id"]
    # services = await check_video_services(session, kp_id)

    # if await check_video_services(session, kp_id) == True:
    #     print(True)
    save_movie_to_db(movie)


async def get_total_pages(session: httpx.AsyncClient, page: int, year: int):
    for token in kp_tokens:
        print(year)
        
        # url = f'https://api.kinopoisk.dev/v1.4/movie?page={page}&limit=250&selectFields=id&selectFields=externalId&selectFields=name&selectFields=enName&selectFields=alternativeName&selectFields=names&selectFields=description&selectFields=shortDescription&selectFields=type&selectFields=typeNumber&selectFields=isSeries&selectFields=status&selectFields=year&selectFields=releaseYears&selectFields=rating&selectFields=ageRating&selectFields=votes&selectFields=budget&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&selectFields=fees&selectFields=premiere&selectFields=sequelsAndPrequels&selectFields=watchability&selectFields=lists&selectFields=top10&selectFields=updatedAt&type=movie&year={year}&selectFields=top250'
        
        headers = {"X-API-KEY": token}
        
        url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit=250&year={year}"

        try:
            response = await session.get(url, headers=headers)
            # print(response.json())
            response.raise_for_status()

            return response.json().get('pages', 0)
        except Exception as e:
            print(f"Kinopoisk error (page {page}): {str(e)}")
            return []
    

async def main():

    async with httpx.AsyncClient(timeout=30) as session:
        # Получаем фильмы с Kinopoisk
        all_movies = []
        year = 2013
        total_pages = await get_total_pages(session, 1, year) # Замените на реальное количество страниц
        # total_pages = 190
        start_page = 1
        print(" Всего страниц:", total_pages)
        
        
        # Собираем все фильмы
        for page in range(start_page, total_pages + 1):
            movies = await fetch_kinopoisk_movies(session, page, year)
            all_movies.extend(movies)
        
        # Обрабатываем фильмы с прогресс-баром
        with tqdm(total=len(all_movies), desc="Processing movies") as pbar:
            tasks = []
            
            for i in range(0, len(all_movies), BATCH_SIZE):
                batch = all_movies[i:i+BATCH_SIZE]

                # Создаем задачи для батча
                for movie in batch:
                    task = save_movie(session, movie, pbar)                 
                    tasks.append(task)
                
                # Выполняем батч
                await asyncio.gather(*tasks)
                pbar.update(10)
                tasks = []
                
                # Пауза между батчами
                await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())