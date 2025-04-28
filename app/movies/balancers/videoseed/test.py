import math
import httpx
import json
import asyncio
from tqdm import tqdm
import pprint
import requests
import json
from db import SessionLocal
from model import Movie

db = SessionLocal() 

async def videoseed(db=None, release_year_from: int=2025, release_year_to: int=2025, items: int=20, page: int=1):

    url = 'https://api.videoseed.tv/apiv2.php'
 
    headers = { 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    params = {
        'list': 'movie',
        'token': 'd503c3e71a5c120705c9c591ef734119',
        'release_year_from': 2024,
        'release_year_to': 2024,
        'items': 50,
        'from': 1
    }

    movies_list = []

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # Первый запрос для получения информации о страницах
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            movies_count = int(data.get('total', 0))
            page_count = math.ceil(movies_count / params['items'])

            print(f"Всего фильмов: {movies_count}, страниц: {page_count}")
            
            pbar = tqdm(total=page_count, desc="Обработка страниц", unit="page")
            
            # Создаем задачи для всех страниц
            tasks = []
            for page in range(1, page_count + 1):

                params = {
                    'list': 'movie',
                    'token': 'd503c3e71a5c120705c9c591ef734119',
                    'release_year_from': 2024,
                    'release_year_to': 2024,
                    'items': 50,
                    'from': page
                }

                tasks.append(client.get(url, headers=headers, params=params))
            
            # Обрабатываем задачи батчами
            BATCH_SIZE = 5
            for i in range(0, len(tasks), BATCH_SIZE):
                batch = tasks[i:i+BATCH_SIZE]
                responses = await asyncio.gather(*batch, return_exceptions=True)
                
                for response in responses:
                    if isinstance(response, Exception):
                        pbar.write(f"Ошибка: {str(response)}")
                        continue
                        
                    try:
                        resp_data = response.json()
                        movies_list.append(resp_data['data'])
                        pbar.update(1)
                    except Exception as e:
                        pbar.write(f"Ошибка парсинга: {str(e)}")
                
                await asyncio.sleep(1)  # Задержка между батчами

            pbar.close()
            
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
        finally:
            with open('movies_data.json', 'w', encoding='utf-8') as f:
                json.dump(movies_list, f, ensure_ascii=False, indent=4)
            print(f"Сохранено записей: {len(resp_data)}")

if __name__ == '__main__':
    asyncio.run(videoseed(db))