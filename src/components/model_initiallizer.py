# SBERT Model Init.
import os
import sys 

from sentence_transformers import SentenceTransformer
from src.logger import logging
from src.exceptions import CustomException

from dataclasses import dataclass

@dataclass
class Model_config:
    model_file_path : str = os.path.join("artifacts\\model", "SBERT_model.pkl")

class Model:
    def __init__(self):
        self.configs = Model_config()
    
    def Initilize_model(self):
        try:
            logging.info("Model Initiallization Started")
            model = SentenceTransformer("all-MiniLM-L6-v2")
            logging.info("Model Initiallized successfully")
            return model
        except Exception as e:
            raise CustomException(e, sys)
    