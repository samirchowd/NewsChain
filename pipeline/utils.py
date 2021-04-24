# utils.py
# Class containing code for all utility functions 

import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import pandas as pd
import glob as g
import time

files = g.glob("../DataBase/data/*.csv")


def toframe(files, attribute):
    """Generate pandas data frame from article csv

    Positional Arguments:
    files -- file path for article csv's
    """

    col_names = ['title', 'abstract', 'author', 'source', 'time_stamp', 'link', 'query']
    articles = []
    for filename in files:
        articles.append(pd.read_csv(filename, names=col_names))

    article_frame = pd.concat(articles, ignore_index=True)
    article_frame.drop_duplicates(['title'], inplace=True)

    # hash function to generate article id. Uses link, because it is a unique value for each article
    key_vals = []
    for i, row in article_frame.iterrows():
        key = hash(row['link'])
        if key not in key_vals:
            key_vals.append(key)
        else:
            key = hash(row['title'])
            if key not in key_vals:
                key_vals.append(key)

    article_frame.insert(loc=0, column='article_id', value=key_vals)
    #query_frame = article_frame[articles['query']].str.contains('sample_query')
    sentenceList = article_frame[attribute].tolist()
    return sentenceList

def encode(text, model):
    """Encode a set of text given an encoding model

    Positional Arguments:
    text -- set of articles to be encoded
    model -- model generated from sentence_transformers
    a fixed-sized output representation (vector u) accomplished by pooling
    """
    start_time = time.time()
    end_time = time.time()
    model.max_seq_length = 300
    sentence_embedding = model.encode(text, convert_to_tensor=True)
    print("Time for computting embeddings:" + str(end_time - start_time))
    return sentence_embedding

# sentenceList = toframe(files, 'abstract')
# roberta = SentenceTransformer('stsb-roberta-base')
# embedding = encode(sentenceList, roberta)


def doc_sim(v1, v2):
    """Find the similarity between two articles

    Positional Arguments:
    v1 -- vector pertaining to the first article
    v2 -- vector pertaining to the second article
    """

    return cosine_similarity(v1.reshape(1,-1),v2.reshape(1,-1))[0][0]

def ent_sim(e1, e2):
    pass

def eos(doc_sim, ent_sim, alpha):
    return (alpha*doc_sim) + ((1-alpha)*ent_sim)

def get_entities(text, conf = 0.35):
    """Returns a set of entities given a text and a model

    Positional Arguments:
    text -- article to extract entites from
    model -- model generated from spacy
    """
    import requests
    class APIError(Exception):
        def __init__(self, status):
            self.status = status
            def __str__(self):
                return "APIError: status={}".format(self.status)

    # Base URL for Spotlight API
    base_url = "http://api.dbpedia-spotlight.org/en/annotate"# Parameters
    # 'text' - text to be annotated
    # 'confidence' -   confidence score for linking
    params = {"text": text, "confidence": conf}# Response content type
    headers = {'accept': 'application/json'}# GET Request
    res = requests.get(base_url, params=params, headers=headers)
    if res.status_code != 200:
        # Something went wrong
        raise APIError(res.status_code)# Display the result as HTML in Jupyter Notebook
    return res

def cluster():
    pass

