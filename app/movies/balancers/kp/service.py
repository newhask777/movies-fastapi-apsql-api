from db import SessionLocal
from model import Movie

db = SessionLocal() 


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
            rating=item.get("rating", {}),
            votes=item.get("votes", {}),
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