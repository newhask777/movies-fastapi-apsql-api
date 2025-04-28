import asyncio
import json
import httpx
from sqlalchemy.orm import Session
from tqdm import tqdm
from db import SessionLocal
from model import Movie

# Конфигурация
YEAR = 2025
BATCH_SIZE = 5
# KINOPOISK_API_KEY = "2BXP44B-HS3460R-JK4BV1F-WX08GD5" 
# KINOPOISK_API_KEY = "5PV2AF3-NC1M1R8-MMXYPP6-HY7NN2X" 
# KINOPOISK_API_KEY = "RJFHMJ6-NCMMB18-Q9909GP-D8R7AGR" 
KINOPOISK_API_KEY = "GDK9FDJ-Y7V4096-N4XFK29-9EX38VQ"
VIDEOCDN_API_KEY = "lTf8tBnZLmO0nHTyRaSlvGI5UH1ddZ2f"
VIDEOSEED_TOKEN = "d503c3e71a5c120705c9c591ef734119"

db = SessionLocal()

async def fetch_kinopoisk_movies(session: httpx.AsyncClient, page: int):
    YEAR = 2025
  
    url = f'https://api.kinopoisk.dev/v1.4/movie?page={page}&limit=250&selectFields=id&selectFields=externalId&selectFields=name&selectFields=enName&selectFields=alternativeName&selectFields=names&selectFields=description&selectFields=shortDescription&selectFields=type&selectFields=typeNumber&selectFields=isSeries&selectFields=status&selectFields=year&selectFields=releaseYears&selectFields=rating&selectFields=ageRating&selectFields=votes&selectFields=budget&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&selectFields=fees&selectFields=premiere&selectFields=sequelsAndPrequels&selectFields=watchability&selectFields=lists&selectFields=top10&selectFields=updatedAt&type=movie&year=2025&selectFields=top250'

    # url = "https://api.kinopoisk.dev/v1.4/movie"

    # params = {
    #     "page": page,
    #     "limit": 250,
    #     "year": YEAR,
    #     "type": "movie",
    #     "selectFields": ",".join([
    #         "id", "externalId", "name", "enName", "alternativeName", "names",
    #         "description", "shortDescription", "slogan", "type", "typeNumber",
    #         "isSeries", "status", "year", "releaseYears", "rating", "ratingMpaa",
    #         "ageRating", "votes", "seasonsInfo", "budget", "audience", "movieLength",
    #         "seriesLength", "totalSeriesLength", "genres", "countries", "poster",
    #         "backdrop", "logo", "ticketsOnSale", "videos", "networks", "persons",
    #         "facts", "fees", "premiere", "sequelsAndPrequels", "watchability",
    #         "lists", "top10", "top250", "updatedAt", "createdAt"
    #     ])
    # }
    
    headers = {"X-API-KEY": KINOPOISK_API_KEY}
    
    try:
        response = await session.get(url, headers=headers)
        # print(response.json())
        response.raise_for_status()
        return response.json().get("docs", [])
    except Exception as e:
        print(f"Kinopoisk error (page {page}): {str(e)}")
        return []


async def check_video_services(session: httpx.AsyncClient, kp_id: int):
    try:
        videocdn_url = f"https://portal.lumex.host/api/short?api_token={VIDEOCDN_API_KEY}&kinopoisk_id={kp_id}"
        videoseed_url = f'https://api.videoseed.tv/apiv2.php?item=movie&token={VIDEOSEED_TOKEN}&kp={kp_id}'


        videocdn_res = await asyncio.gather(
            session.get(videocdn_url)
        )

        videoseed_res = await asyncio.gather(
            session.get(videoseed_url)
        )

        vdcdn_response = videocdn_res[0].json()  # Первый (и единственный) ответ
        vdseed_response = videoseed_res[0].json()  # Первый (и единственный) ответ

        
        try:
            print(vdcdn_response)
            print(vdseed_response)
                      
        except Exception as e:
            print(f"Ошибка декодирования JSON: {e}")
           

        # if(videocdn_res[0].json()['result'] != False or videoseed_res[0].json()["status"] != 'error'):
        if(videocdn_res):
            print("Movie ===========================================================================")
            return True
        
    except Exception as e:
        print(f"Video services check error (ID {kp_id}): {str(e)}")
        return {"exists_in_videocdn": False, "exists_in_videoseed": False}
    
    
def save_movie_to_db(item: dict):
    try:
        movie = Movie(
            kp_id=item["id"],
            name=item.get("name"),
            alt_name=item.get("alternativeName"),
            en_name=item.get("enName"),
            type=item.get("type"),
            type_number=item.get("typeNumber"),
            year=item.get("year"),
            description=item.get("description"),
            short_description=item.get("shortDescription"),
            status=item.get("status"),
            rating=item.get("rating", {}).get("kp"),
            votes=item.get("votes", {}).get("kp"),
            movie_length=item.get("movieLength"),
            age_rating=item.get("ageRating"),
            poster=item.get("poster", {}),
            genres=item.get("genres", []),
            countries=item.get("countries", []),
            persons=item.get("persons", []),
            budget=item.get("budget", {}),
            fees=item.get("fees", {}),
            premier=item.get("premiere", {}),
            seq_and_preq=item.get("sequelsAndPrequels", []),
            watchability=item.get("watchability", {}),
            top10=item.get("top10"),
            top250=item.get("top250"),
            tickets_on_sale=item.get("ticketsOnSale"),
            lists=item.get("lists", [])
        )
        
        db.add(movie)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении фильма {item.get('id')}: {str(e)}")


async def process_movie(session: httpx.AsyncClient, movie: dict, pbar: tqdm):
    kp_id = movie["id"]
    services = await check_video_services(session, kp_id)

    if await check_video_services(session, kp_id) == True:
        print(True)
        save_movie_to_db(movie)

    
    
async def main():

    async with httpx.AsyncClient(timeout=30) as session:
        # Получаем фильмы с Kinopoisk
        all_movies = []
        total_pages = 7  # Замените на реальное количество страниц
        
        # Собираем все фильмы
        for page in range(1, total_pages + 1):
            movies = await fetch_kinopoisk_movies(session, page)
            all_movies.extend(movies)
        
        # Обрабатываем фильмы с прогресс-баром
        with tqdm(total=len(all_movies), desc="Processing movies") as pbar:
            tasks = []
            
            for i in range(0, len(all_movies), BATCH_SIZE):
                batch = all_movies[i:i+BATCH_SIZE]
                
                # Создаем задачи для батча
                for movie in batch:
                    task = process_movie(session, movie, pbar)
                    tasks.append(task)
                
                # Выполняем батч
                await asyncio.gather(*tasks)
                tasks = []
                
                # Пауза между батчами
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())