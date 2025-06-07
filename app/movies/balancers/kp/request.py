import pprint
import requests
import json
from db import SessionLocal
from model import Movie

db = SessionLocal() 

year = 2020
balanser = []
# KINOPOISK_API_KEY = "2BXP44B-HS3460R-JK4BV1F-WX08GD5", # exp newhaskellisp 
# KINOPOISK_API_KEY = "5PV2AF3-NC1M1R8-MMXYPP6-HY7NN2X"# haskellisp
KINOPOISK_API_KEY = "RJFHMJ6-NCMMB18-Q9909GP-D8R7AGR" # ivanhask369
# KINOPOISK_API_KEY = "GDK9FDJ-Y7V4096-N4XFK29-9EX38VQ" # barakdimon  
# KINOPOISK_API_KEY = "TSG399W-WJ7MSTM-NET4M6F-6EN5ZBA" # lehazarutel 
# KINOPOISK_API_KEY = "4NAC79D-8YY4WEJ-MGTBHM1-AF3WMR4" # hanzfierman 
# KINOPOISK_API_KEY = "A287HMK-ZKTMKHR-MFJQNJ8-FC6YPJS" # petermuller

for i in range(188, 225):

    print(i)

    url = f'https://api.kinopoisk.dev/v1.4/movie?page={i}&limit=250&selectFields=id&selectFields=externalId&selectFields=name&selectFields=enName&selectFields=alternativeName&selectFields=names&selectFields=description&selectFields=shortDescription&selectFields=slogan&selectFields=type&selectFields=typeNumber&selectFields=isSeries&selectFields=status&selectFields=year&selectFields=releaseYears&selectFields=rating&selectFields=ratingMpaa&selectFields=ageRating&selectFields=votes&selectFields=seasonsInfo&selectFields=budget&selectFields=audience&selectFields=movieLength&selectFields=seriesLength&selectFields=totalSeriesLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=backdrop&selectFields=logo&selectFields=ticketsOnSale&selectFields=videos&selectFields=networks&selectFields=persons&selectFields=facts&selectFields=fees&selectFields=premiere&selectFields=sequelsAndPrequels&selectFields=watchability&selectFields=lists&selectFields=top10&selectFields=top250&selectFields=updatedAt&selectFields=createdAt&type=movie&year={year}'

    headers = {
        "X-API-KEY": KINOPOISK_API_KEY
    }

    params = {

    }

    response = requests.get(url, headers=headers).json()
    

    for item in response["docs"]:

        # movie_count +=1
        # print(movie_count)
        print(item['id'])

        # videocdn_url = f'https://videocdn.tv/api/movies?api_token=lTf8tBnZLmO0nHTyRaSlvGI5UH1ddZ2f&kinopoisk_id={item["id"]}'
        # videocdn_request = requests.get(videocdn_url).json()

        # # videoseed_url = f'https://api.videoseed.tv/apiv2.php?item=movie&token=d503c3e71a5c120705c9c591ef734119&kp={item["id"]}'
        # # videoseed_request = requests.get(videoseed_url).json()

        # # pprint.pprint(videoseed_request['data'])
        # pprint.pprint(videocdn_request)
        

        # if(item):
            # print('True')
            # pprint.pprint(videoseed_request)
            # pprint.pprint(videocdn_request)
            # balanser.append(videocdn_request)
            # balanser.append(videoseed_request)
        try:  
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
        except:
            continue

# with open('videoseed.json', 'w', encoding='utf-') as f:
#     json.dump(balanser, f, indent=4, ensure_ascii=False)



