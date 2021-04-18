import scrapy
import csv
import json
from pprint import pprint


def loadSites(query, requests, endRequests):
    result = []
    for x in range(requests, endRequests):
        result.append("https://api.thenewsapi.com/v1/news/all?search=" + query + "&page=" + str(x) + "&published_after=2019-01-01&published_before=2021-03-01&language=en&api_token=Z8GmjFjQN6jTs63dyWulFhD4QTm1GcA3PbxTsl2N")
    return result

class theNewsAPI(scrapy.Spider):
    name = 'theNews'
    allowed_domains = ['thenewsapi.com/']
    query = "covid"
    start_urls = loadSites(query, 61, 141)
    output = "theNewsAPI2.csv"

    def parse(self, response):
        query = self.query
        with open(self.output, "a", newline="") as f:
            writer = csv.writer(f)
            results = json.loads(response.body)
            for article in results['data']:
                try:
                    headline = article['title']
                except:
                    headline = ""
                try:
                    abstract = article['description']
                except:
                    abstract = ""
                try:
                    source = article['source']
                except:
                    source = ""
                try:
                    date = article['published_at']
                except:
                    date = ""
                try:
                    url = article['url']
                except:
                    url = ""
                try:
                    categories = article['categories']
                except:
                    categories = ""

                writer.writerow([headline, abstract, source, date, url, categories, query])
                yield {'headline': headline, 'abstract': abstract, 'source': source, 'date': date, 'url': url, 'categories': categories}