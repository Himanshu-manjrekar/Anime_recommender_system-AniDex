# code to predict the input and give the recommendation


from dataclasses import dataclass
from src.utils import *
from src.components.model_initiallizer import Model_config
from src.components.data_modelling import DataModeller_config
from src.pipeline.train_pipeline import trainning_config

@dataclass
class prediction_config:
    model_path: str = Model_config.model_file_path
    df_path: str = DataModeller_config.dataframe_file_path
    embedding_matrix_path: str = trainning_config.embedding_matrix_path


class Prediction:
    def __init__(self):
        self.configs = prediction_config()
        self.model = load_obj(self.configs.model_path, object_name="SBERT Model")
        self.df = load_obj(self.configs.df_path, object_name="Anime Data Frame")
        self.embedding_matrix = load_obj(self.configs.embedding_matrix_path, object_name = "Embedding Matrix")
    
    
    def perform_prediction(self, user_query):
        user_query_embedding = get_embedding(user_query, model = self.model)
        top_k_indices = cal_similarity(user_query_embedding, self.embedding_matrix)
        recommendation = self.df.iloc[top_k_indices][["title_default", "synopsis"]]
        return recommendation

