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

data = toframe(files)
d = data[data['query'].str.contains('pfizer')]
print(d)

def encode(text, model, max_seq_length = 300):
    """Encode a set of text given an encoding model

    Positional Arguments:
    text -- set of articles to be encoded
    model -- model generated from sentence_transformers
    a fixed-sized output representation (vector u) accomplished by pooling
    """
    start_time = time.time()
    model.max_seq_length = max_seq_length 
    sentence_embedding = model.encode(text)
    end_time = time.time()
    print("Time for computting embeddings:" + str(end_time - start_time))
    return sentence_embedding

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
    
    return set([x['@URI'] for x in bruh['Resources']])

def cluster():
    pass

#tuple = (title, abstract, author, source, date, URL, query)
doc1 = ['Three Men Are Accused in Scheme to Sell Covid-19 Vaccines', 'Prosecutors said the men created a fake duplicate of the Moderna website to fraudulently sell doses of the vaccine, which they never had.', 'John', 'NY Times', 'april 23', 'sample_url', 'moderna']
doc2 = ['title2', 'Four Men Are Talking About Covid-19 Vaccines', 'Jack', 'Washington Post', 'march 15', 'sample_url2', 'pfizer']

def vectorize(dx):  # Modify this function
    list_x = dx.split()
    vx = np.array(list_x)

    return vx

def docSim(abstract_i, abstract_j):
    roberta = SentenceTransformer('stsb-roberta-base')

    vi = utils.encode(abstract_i, roberta)
    vj = utils.encode(abstract_j, roberta)
    cosine_similarity = 1 - spatial.distance.cosine(vi, vj)
    return cosine_similarity

def knowledgeSim(abstract_i, abstract_j):
    vi = vectorize(abstract_i)
    vj = vectorize(abstract_j)
    jaccard_similarity = spatial.distance.jaccard(vi, vj)
    jaccard_distance = 1 - jaccard_similarity
    return jaccard_distance

def Compute_EOS(di, dj, alpha):  # di, dj are 7-tuples, whose 2nd element is abstract

    doc_sim = docSim(di[1], dj[1])
    knowledge_sim = knowledgeSim(di[1], dj[1])
    eos = alpha * doc_sim + (1 - alpha) * knowledge_sim
    return eos

# vec1 = [0, 1, 7]
# vec2 = [15, 6, 9]
# print(docSim(vec1, vec2))
#print(Compute_EOS(doc1, doc2, 0.3))


if __name__ == '__main__':
    data = utils.toframe(utils.files, 'abstract', 'pfizer')
    print(data[0])