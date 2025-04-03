
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.components.data_ingestion import DataIngest
from src.components.data_modelling import Model_data
from src.components.model_initiallizer import Model
from src.pipeline.train_pipeline import start_trainning
from src.pipeline.predict_pipeline import Prediction
from src.utils import save_obj, load_obj


if __name__ == "__main__":
    print("Builder kicked In")
    # data Ingestion
    # data_ingestor = DataIngest() 
    # raw_animes_dict = data_ingestor.initiate_data_ingestion()                       # animes will be stored in "animes"
    # save_obj(file_path = data_ingestor.configs.anime_obj_file_path , obj = raw_animes_dict, object_name="Animes Dictionary") # save animes dictionary in pickle
    # animes_data = load_obj(data_ingestor.configs.anime_obj_file_path, object_name="Animes Dictionary") # we need to load the saved raw animes dictionary and then pass it to modeller to create df
    
    # data Modelling
    # data_modeller = Model_data()  
    # df = data_modeller.build_data_frame(animes_data)                          # build the animes dataframe
    # df = data_modeller.transform_data(df)                                     # transform the Data (preproces)
    # save_obj(file_path = data_modeller.configs.dataframe_file_path, obj = df, object_name="Preprocessed Data") # save the Dataframe
    # anime_df = load_obj(data_modeller.configs.dataframe_file_path, object_name="Preprocessed Data")

    # SBERT model
    # model = Model()
    # sbert = model.Initilize_model()                                                 # initialize and load the SBERT model
    # save_obj(file_path = model.configs.model_file_path, obj = sbert, object_name="SBERT model")                                  # save the SBERT model
    # sbert_model = load_obj(model.configs.model_file_path, object_name="SBERT model")
    

    # Start encoding the synopsis
    # trainning = start_trainning(anime_df, sbert_model)
    # embed_matrix = trainning.build_embedding_matrix()
    # save_obj(file_path = trainning.configs.embedding_matrix_path, obj = embed_matrix, object_name = "Embedding Matrix")

    # Perform prediction
    prediction = Prediction()
    user_input = "a guy finds a notebook that can kill people by writing their name and death reason on it"
    print(prediction.perform_prediction(user_input))
    print("Builder Actions Completed.")