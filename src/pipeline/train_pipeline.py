# Code to encode the updated Synopsis from the dataframe and saving it 
import numpy as np
import os
import sys

from src.utils import save_obj
from src.logger import logging
from src.exceptions import CustomException
from dataclasses import dataclass

@dataclass
class trainning_config:
    embedding_matrix_path: str = os.path.join("src\\components\\artifacts\\embedding_matrix", "embedding_matrix.pkl")
    updated_df_file_path: str= os.path.join("src\\components\\artifacts\\data\\data_frame", "Anime_data_final.pkl")

class start_trainning():
    def __init__(self, df, model):
        self.configs = trainning_config()
        self.df = df
        self.model = model

    def encode_synopsis(self):
        try:
            # embedding the synopsis
            logging.info("Creating Embeddings of synopsis") 
            self.df["embeddings"] = self.df["updated_synopsis"].apply(lambda x: self.model.encode(x, show_progress_bar=False))
            logging.info("Embeddings created Successfully")
            logging.info("Saving the Updated data frame") 
            save_obj(file_path = self.configs.updated_df_file_path, obj = self.df, object_name="Data along with embeddings of synopsis")
            logging.info(f"Updated Dataframe saved successfully at {self.configs.updated_df_file_path}")
            return self.df["embeddings"]
        except Exception as e:
            raise CustomException(e, sys)
    
    def build_embedding_matrix(self):
        try:
            logging.info("Building the embedding matrix")
            embeddings_col = self.encode_synopsis()
            embedding_matrix = np.vstack(embeddings_col.values)
            logging.info("Embedding matrix built successfully")
            return embedding_matrix
        except Exception as e:
            raise CustomException(e, sys)
    
    def save_embeddings(self):
        try:
            embedding_matrix = self.build_embedding_matrix()
            logging.info(f"Saving the Embedding Matrix at {self.configs.embedding_matrix_path}")
            save_obj(file_path = self.configs.embedding_matrix_path, obj = embedding_matrix, object_name="Embedding matrix")
        except Exception as e:
            raise CustomException(e, sys)