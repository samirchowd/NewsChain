# utils.py
# Class containing code for all utility functions 

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

def encode(text, model):
    """Encode a set of text given an encoding model
    
    Positional Arguments:
    text -- set of articles to be encoded
    model -- model generated from sentence_transformers
    """
    
    return model.encode(text)
    
def doc_sim(v1, v2):
    """Find the similarity between two articles
    
    Positional Arguments:
    v1 -- vector pertaining to the first article
    v2 -- vector pertaining to the second article 
    """
    
    return cosine_similarity(v1.reshape(1,-1),v2.reshape(1,-1))[0][0]

def ent_sim(a1, a2):
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
    params = {"text": text, "confidence": conf}# Response content type
    headers = {'accept': 'application/json'}# GET Request
    res = requests.get(base_url, params=params, headers=headers)
    if res.status_code != 200:
        # Something went wrong
        raise APIError(res.status_code)# Display the result as HTML in Jupyter Notebook
    return res 

def cluster():
    pass


