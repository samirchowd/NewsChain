# utils.py
# Class containing code for all utility functions 
import utils
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import pandas as pd
import glob as g
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import spatial

files = g.glob("../DataBase/data/*.csv")


def toframe(files, attribute=None, query=None):
    """Generate pandas data frame from article csv
    Positional Arguments:
    files -- file path for article csv's
    Valid queries: 'pfizer', 'moderna', 'Johnson and Johnson', 'Johnson', 'Johnson & Johnson', 'covid', 'coronavirus', 'vaccine', 'covid 19'
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
    af = article_frame.dropna()

    if attribute is not None and query is not None:
        query_frame = af[af['query'].astype(str).str.contains(query)]
        sentenceList = query_frame[attribute].tolist()
        return sentenceList
    elif attribute is not None:
        sentenceList = af[attribute].tolist()
        return sentenceList
    elif query is not None:
        temp_list = list()
        fl = []
        query_frame = af[af['query'].str.contains(query)]
        for col in query_frame:
            temp_list = article_frame[col].tolist()
            fl.append(temp_list)
        return fl
    else:
        return af

def encode(text, model, max_seq_length = 300):
    """Encode a set of text given an encoding model

    Positional Arguments:
    text -- set of articles to be encoded
    model -- model generated from sentence_transformers
    a fixed-sized output representation (vector u) accomplished by pooling
    """
    model.max_seq_length = max_seq_length 
    sentence_embedding = model.encode(text)
    return sentence_embedding

def doc_sim(v1, v2):
    """Find the similarity between two articles

    Positional Arguments:
    v1 -- vector pertaining to the first article
    v2 -- vector pertaining to the second article
    """

    return cosine_similarity(v1.reshape(1,-1),v2.reshape(1,-1))[0][0]

def knowledge_sim(article_i, article_j):
    ai = get_ents(article_i.lower())
    aj = get_ents(article_j.lower())

    union = ai.union(aj)
    intersect = ai.intersection(aj)

    jaccard_coefficient = len(intersect) / len(union)
    return jaccard_coefficient

def eos(a1, a2, alpha, model):
    v = utils.encode([a1, a2], model)
    ds = utils.doc_sim(v[0], v[1])
    ks = utils.knowledge_sim(a1, a2)
    return (alpha*ds) + ((1-alpha)*ks)

def get_ents(text, confidence= 0.35):
    import requests
    from IPython.core.display import display, HTML# An API Error Exception
    class APIError(Exception):
        def __init__(self, status):
            self.status = status
            def __str__(self):
                return "APIError: status={}".format(self.status)

    # Base URL for Spotlight API
    base_url = "http://api.dbpedia-spotlight.org/en/annotate"# Parameters 
    # 'text' - text to be annotated 
    # 'confidence' -   confidence score for linking
    params = {"text": text, "confidence": confidence}# Response content type
    headers = {'accept': 'application/json'}# GET Request
    res = requests.get(base_url, params=params, headers=headers)
    if res.status_code != 200:
        # Something went wrong
        raise APIError(res.status_code)# Display the result as HTML in Jupyter Notebook
    
    import json 
    bruh = json.loads(res.content)

    try:
        return set([x['@URI'] for x in bruh['Resources']])
    except:
        return set()

def find_article(links, data):
    """Find input article in dataset

     Positional Arguments:
     link -- link of input article
     data -- original data frame

     Return:
     pandas dataframe where each row in the frame is an attribute
     """
    art = pd.DataFrame()
    for index, row in data.iterrows():
        if row['link'] in links:
            art = art.append(row)
    return art


def relate(data, inp, model, theta1 = 0.5, alpha = 0.45):
#     list = pd.DataFrame()
#     for index, row in data.iterrows():
#         rt = row['title']
#         for i in inp['title']:
#             v2 = utils.encode(i, model)
#             sim_value = utils.doc_sim(v1, v2)
#             if sim_value > theta1:
#                 list = list.append(row)
                
    df = pd.DataFrame()
    
    ctext = []
    for index, art in inp.iterrows():
        ctext.append(art['title'] + ': ' + art['abstract'])
    
    for _, row in data.iterrows():
        rt = row['title'] + ': ' + row['abstract']
        for ct in ctext:
            if utils.eos(rt, ct, alpha, model) > theta1:
                df = df.append(row)
                
    return df

