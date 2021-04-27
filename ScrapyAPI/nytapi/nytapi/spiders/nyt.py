import scrapy
import csv
import json
from pprint import pprint


def loadSites(query, start):
    result = []
    for x in range(start, start + 10):
        result.append("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + query + "&page=" + str(x) + "&begin_date=20190101&end_date=20210301&api-key=CnAxA1q2BGHoUPJ1CBYy9WEKmhkvQH6W")
    return result

class NytSpider(scrapy.Spider):
    name = 'nyt'
    query = '"Johnson & Johnson" OR "Johnson and Johnson"'
    start_urls = loadSites(query, 00)
    output = "newCSV.csv"

    #def __init__(self, pagenum=0, **kwargs):
        #query = self.query
        #self.allowed_domains = ['api.nytimes.com']
        #self.start_urls = [f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&page={pagenum}&begin_date=20190101&end_date=20210301&api-key=CnAxA1q2BGHoUPJ1CBYy9WEKmhkvQH6W']  # py36
        #super().__init__(**kwargs)

    def parse(self, response):
        query = self.query
        with open(self.output, "a", newline="") as f:
            writer = csv.writer(f)
            results = json.loads(response.body)
            for article in results['response']['docs']:
                try:
                    headline = article['headline']['main']
                except:
                    headline = ""
                try:
                    abstract = article['abstract']
                except:
                    abstract = ""
                try:
                    author = article['byline']['original']
                except:
                    author = ""
                try:
                    source = article['source']
                except:
                    source = ""
                try:
                    date = article['pub_date']
                except:
                    date = ""
                try:
                    url = article['web_url']
                except:
                    url = ""

                writer.writerow([headline, abstract, author, source, date, url, query])
                yield {'headline': headline, 'abstract': abstract, 'author': author, 'source': source, 'date': date, 'url': url}