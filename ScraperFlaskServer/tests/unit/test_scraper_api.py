from ScraperFlaskServer.XP_Scraper.ScraperAPI import ScraperAPI
from ScraperFlaskServer.XP_Scraper.spiders.default import DefaultSpider
from ScraperFlaskServer.XP_Scraper.spiders.reuters import ReutersSpider


def test_scraperApiInit():
  scraper = ScraperAPI()
  assert scraper.results == []

def test_getSpiderList():
  scraper = ScraperAPI()
  assert scraper.getSpiderList() != None

def test_getRelevantSpider_default():
  scraper = ScraperAPI()
  assert scraper.getRelevantSpider("someString") == DefaultSpider

def test_getRelevantSpider_notDefault():
  scraper = ScraperAPI()
  assert scraper.getRelevantSpider("www.reuters.com").__name__ == ReutersSpider.__name__

def test_crawlerResults():
  scraper = ScraperAPI()
  someList = {"hello":"yes"}
  scraper.crawlerResults(someList)
  assert scraper.results == list(someList)


# I have no idea how to build unit tests for these yet
# TO DO:
# def test_loadSpider():
# def test_runSpiders():
# def test_dispatchSpiders():