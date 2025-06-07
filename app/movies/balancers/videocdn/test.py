import httpx
import json
import asyncio
from tqdm import tqdm
import pprint

import json
from service import save_movie_to_db

async def videocdn():

    api_token = 'lTf8tBnZLmO0nHTyRaSlvGI5UH1ddZ2f'

    # url = f'https://portal.lumex.host/api/movies?api_token=lTf8tBnZLmO0nHTyRaSlvGI5UH1ddZ2f&direction=desc&limit=100&page=1'
    url = f'https://portal.lumex.host/api/movies'
 
    headers = { 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    params = {
        'api_token': api_token,
        'direction': 'asc',
        'limit': 100,
        'page': 1
    }

    movies_list = []

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # Первый запрос для получения информации о страницах
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            movies_count = data.get('total', 0)
            page_count = data.get('last_page', 0)
            # page_count = 10

            print(movies_count, page_count)

            print(f"Всего фильмов: {movies_count}, страниц: {page_count}")
            
            pbar = tqdm(total=page_count, desc="Обработка страниц", unit="page")
            
            # Создаем задачи для всех страниц
            tasks = []
            for page in range(1, page_count + 1):

                params = {
                    'api_token': api_token,
                    'direction': 'desc',
                    'limit': 100,
                    'page': page
                }

                tasks.append(client.get(url, headers=headers, params=params))
            
            # Обрабатываем задачи батчами
            BATCH_SIZE = 10
            for i in range(0, len(tasks), BATCH_SIZE):
                batch = tasks[i:i+BATCH_SIZE]
                responses = await asyncio.gather(*batch, return_exceptions=True)
                
                for response in responses:
                    if isinstance(response, Exception):
                        pbar.write(f"Ошибка: {str(response)}")
                        continue
                        
                    try:
                        resp_data = response.json()['data']
                        # movies_list.append(resp_data)

                        for item in resp_data:

                            save_movie_to_db(item)

                        pbar.update(1)
                    except Exception as e:
                        pbar.write(f"Ошибка парсинга: {str(e)}")
                
                await asyncio.sleep(1)  # Задержка между батчами

            pbar.close()
            
        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")
        finally:
            with open('json/movies_data.json', 'w', encoding='utf-8') as f:
                json.dump(movies_list, f, ensure_ascii=False, indent=4)
            print(f"Сохранено записей: {len(resp_data)}")

if __name__ == '__main__':
    asyncio.run(videocdn())