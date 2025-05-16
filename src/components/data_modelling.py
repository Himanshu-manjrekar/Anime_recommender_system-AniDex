# code to Transform data (Data Modelling)


# 1. we gonna build a pd Dataframe from animes
# 2. Then apply Transformation on it 
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils import text_cleaner, preprocess_text,handle_english_title, handle_title_synonyms, update_synopsis, clean_synopsis, save_obj
from dataclasses import dataclass
from src.logger import logging
from src.exceptions import CustomException


@dataclass
class DataModeller_config:
    dataframe_file_path: str = os.path.join("src\\components\\artifacts\\data\\data_frame", "Anime_data.pkl")

class Model_data:
    def __init__(self):
        self.configs = DataModeller_config()

    def build_data_frame(self, animes):
        try:
            logging.info("Building the DataFrame")
            df = pd.DataFrame(animes)
            logging.info("Built the Dataframe successfully")
            return df
        except Exception as e:
            raise CustomException(e, sys)
        

    def transform_data(self, df):
        try:
            logging.info("Started transforming the Data.")
            # perform the Transformation on df
            df["title_synonyms"] = df["title_synonyms"].apply(text_cleaner)
            df["title_synonyms"] = df["title_synonyms"].replace("", np.nan)
            
            # df["title_default"].isnull().sum()  # No null Vlaues in this col
            # df["title_english"].isnull().sum()   # 16176 null values -> function that will replace "NaN" value with the original title
            # df["title_synonyms"].isnull().sum()  # 14192 null values -> function that will replace "NaN" value with the original title

            # print("Count of null Before Dropping:- ",df["synopsis"].isnull().sum(), ", Length of Data Frame Before Dropping:- ",len(df))
            # 5084 -> Irrelevant Data drop it
            df = df.dropna(subset = ["synopsis"])
            # print("Count of null After Dropping:- ", df["synopsis"].isnull().sum(), ", Length of Data Frame After Dropping:- ", len(df))

            df["title_english"] = df.apply(handle_english_title, axis =1)
            df["title_synonyms"] = df.apply(handle_title_synonyms, axis = 1)
            logging.info("title english, synonyms column transformation completed.")

            df["updated_synopsis"] = df.apply(update_synopsis, axis = 1)
            df["updated_synopsis"] = df["updated_synopsis"].apply(clean_synopsis)
            logging.info("Cleaning of updated synopsis completed")
            df["updated_synopsis"] = df["updated_synopsis"].apply(preprocess_text)
            logging.info("preprocessing of updated synopsis completed")
            df.reset_index(inplace = True)
            df.drop(columns=["index"], inplace=True)
            logging.info("Data Transformation Completed.")
            return df
        except Exception as e :
            raise CustomException(e,sys)
    
   