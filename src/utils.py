# Here all the Helper functions 
import pandas as pd
import re
import os
import dill
import sys 
import pickle 
import numpy as np

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from src.logger import logging
from src.exceptions import CustomException
from sklearn.metrics.pairwise import cosine_similarity

def text_cleaner(text):
    text = re.sub("[^a-zA-Z0-9]", " ", text)
    text = text.strip()
    return text


def handle_english_title(a):
    if pd.isna(a["title_english"]):
        return a["title_default"]
    return a["title_english"]

def handle_title_synonyms(a):
    if pd.isna(a["title_synonyms"]):
        return a["title_default"]
    return a["title_synonyms"]

def preprocess_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    tokens = word_tokenize(text)  # Tokenization
    tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatization
    return ' '.join(tokens)

def clean_synopsis(a):
    find = "[Written by MAL Rewrite]"
    if find in a:
        a = a.replace(find, "")
        a = a.strip()
        return a
    else:
        a = a.strip()
        return a

def update_synopsis(a):
    if a["title_english"] == a["title_synonyms"]:
        return a["synopsis"] + " " +a["title_english"]
    else:
        return a["synopsis"] + " " + a["title_synonyms"] + " " + a["title_english"]

def save_obj(file_path, obj, object_name):
    try:
        dir_path = os.path.dirname(file_path)
        logging.info(f"{dir_path} Directory path for {object_name}")
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"Saving {object_name}")
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"{object_name} saved successfully at {file_path}")
    except Exception as e:
        raise CustomException(e, sys)


def load_obj(file_path, object_name):
    try:
        logging.info(f"Loading {object_name} from {file_path}")
        with open(file_path, "rb") as f:
            return pickle.load(f)
        logging.info(f"{object_name} Loaded sucessfully.")
    except Exception as e:
        raise CustomException(e, sys)

def get_embedding(text, model):
    processed_text = preprocess_text(text)  # Preprocess input
    return model.encode(processed_text, show_progress_bar = False)  # Convert to vector



def cal_similarity(user_query_embedding, embedding_matrix):
    # Compute Similarity Score
    similarities = cosine_similarity([user_query_embedding], embedding_matrix)[0]
    # get top k recommendations
    top_k_indices = np.argsort(similarities)[::-1][:10]
    return top_k_indices