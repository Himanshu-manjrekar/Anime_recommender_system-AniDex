# Code to ingest data from Jikan API and load in csv file
import requests
import json
import time
import sys
import os

from src.logger import logging
from src.exceptions import CustomException
from dataclasses import dataclass

@dataclass
class DataIngest_config:
    page: int = 1
    base_url: str = "https://api.jikan.moe/v4/"
    anime_obj_file_path: str = os.path.join("artifacts\\data\\raw", "raw_data.pkl")

class DataIngest:
    def __init__(self):
        self.configs = DataIngest_config()

    def initiate_data_ingestion(self):
        # animes dictionary which will be converted to DataFrame
        animes = {
            "mal_id": [],          # store mal_id of Anime
            "title_default": [],   # store default title of Anime
            "title_english": [],   # store English title of Anime
            "title_synonyms": [],  # store Synonyms of title of Anime
            "synopsis": [],        # store description of Anime
            "season": [],          # store season of Anime
            "genres": [],          # store genres of Anime
        }
        try:    
            # an initial request to get "has_next_page" bool value which will be acting as a controller for while loop
            logging.info("Making Initial request to set the next page flag.")
            response = requests.request("GET", self.configs.base_url+"anime")   # API response after hitting the base_url+anime
            response = json.loads(response.text)                   # load response in json for better interoperability
            next_page = response["pagination"]["has_next_page"]    # next_page controller
        except Exception as e:
            raise CustomException(e, sys)

        try:
            logging.info("Data Ingestion Started.")
            while next_page:
                # logging.info("URL :- ",self.base_url+'anime?page='+str(self.page)) # acting as a chceker what URL we are hitting
                # print(("URL :- ",self.configs.base_url+'anime?page='+str(self.configs.page)))
                response = requests.request("GET", self.configs.base_url+'anime?page='+str(self.configs.page))   # hitting the URL w.r.t page number
                response = json.loads(response.text)
                next_page = response["pagination"]["has_next_page"]   # updating the controller value
                data = response["data"]     # getting data from response

                # unloading data from data
                for i in range(len(data)):
                    # appendning data in animes Dictionary
                    animes["mal_id"].append(data[i]["mal_id"])               
                    animes["title_default"].append(data[i]["title"])
                    animes["title_english"].append(data[i]["title_english"])
                    # unpacking title_synonyms into unpacked_titles
                    titles = data[i]["title_synonyms"]
                    unpacked_titles = [] 
                    for _ in titles:
                        unpacked_titles.append(_)
                    animes["title_synonyms"].append(" ".join(unpacked_titles))
                    animes["synopsis"].append(data[i]["synopsis"])
                    animes["season"].append(data[i]["season"])
                    genres = data[i]["genres"]

                    # unpacking genres into genres_fetched
                    genres_fetched = []
                    for j in genres:
                        genres_fetched.append(j["name"])
                    animes["genres"].append(" ".join(genres_fetched))
                
                self.configs.page += 1     # incrementing page counter by 1 
                time.sleep(0.5)  # Wait for 2 seconds to make another request
            logging.info(" Data Ingestion Completed.")
            return animes
        except Exception as e:
            logging.info(e)
