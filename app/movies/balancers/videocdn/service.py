from db import SessionLocal
from model import MovieVCDN


db = SessionLocal() 


def save_movie_to_db(item: dict = None):

    # print('save')
    
    try:
        movie = MovieVCDN(
            videocdn_id = item.get("id"),
            ru_title = item.get("ru_title"),
            orig_title = item.get("orig_title"),
            imdb_id = item.get("imdb_id"),
            kinopoisk_id = item.get("kinopoisk_id"),
            created = item.get("created"),
            released = item.get("released"),
            updated = item.get("updated"),
            iframe_src = item.get("iframe_src"),
            iframe = item.get("iframe"),
            year = item.get("year"),
            content_type = item.get("content_type"),
            media = item.get("media", []),
            translations = item.get("translations", []),
            default_media_id = item.get("default_media_id"),
        )
        
        db.add(movie)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении фильма {item.get('id')}: {str(e)}")