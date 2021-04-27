import utils
import pandas as pd
import numpy as np
import spacy
from sentence_transformers import SentenceTransformer
import glob as g

# Pfizer Seals Deal With U.S. for 100 Million More Vaccine Doses,"The company agreed to deliver the additional doses of its coronavirus vaccine by the end of July, helping address a looming shortage.",By Sharon LaFraniere and Zach Montague,The New York Times,2020-12-23T21:42:07+0000,https://www.nytimes.com/2020/12/23/us/politics/pfizer-vaccine-doses-virus.html,pfizer
# Pfizer Nears Deal With Trump Administration to Provide More Vaccine Doses,The company could provide at least tens of millions of additional doses of a coronavirus vaccine under an agreement that would give it better access to the supplies it needs to expand manufacturing.,By Sharon LaFraniere and Katie Thomas,The New York Times,2020-12-22T21:25:27+0000,https://www.nytimes.com/2020/12/22/us/politics/pfizer-vaccine-doses.html,pfizer
# Biden Pledges to Speed Flow of Vaccines to the States,President Biden said the number of coronavirus vaccines reaching the states would rise next week and a deal was near to provide enough shots to vaccinate nearly all Americans by the end of summer.,"By Sheryl Gay Stolberg, Noah Weiland and Sharon LaFraniere",The New York Times,2021-01-27T00:44:50+0000,https://www.nytimes.com/2021/01/26/us/politics/biden-coronavirus-vaccines.html,pfizer
# Biden Administration Orders 200 Million More Vaccine Doses,President Biden announced on Tuesday that his administration was working on a deal to secure the doses of coronavirus vaccine from Pfizer and Moderna by the end of the summer. The deal is unlikely to accelerate the current pace of vaccination for several months.,By Reuters,The New York Times,2021-01-26T23:10:31+0000,https://www.nytimes.com/video/us/politics/100000007572398/biden-pfizer-moderna-coronavirus-vaccine.html,pfizer

l1 = 'https://www.nytimes.com/2021/01/26/us/politics/biden-coronavirus-vaccines.html'
l2 = 'https://www.nytimes.com/video/us/politics/100000007572398/biden-pfizer-moderna-coronavirus-vaccine.html'

data = utils.toframe(utils.files)
roberta = SentenceTransformer('stsb-roberta-base')
links = set()
links.add(l1)
links.add(l2)

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


def relate(data, input, model, alpha):
    list = pd.DataFrame()
    for index, row in data.iterrows():
        rt = row['title']
        v1 = utils.encode(rt, model)
        for i in input['title']:
            v2 = utils.encode(i, model)
            sim_value = utils.doc_sim(v1, v2)
            if sim_value > alpha:
                list = list.append(row)
    return list

# input = find_article(links, data)
# print(relate(data, input, roberta, 0.8))



