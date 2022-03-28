import json
from pyclbr import Function
from typing import Type
import scrapy.crawler as crawler
from scrapy.utils import project
from scrapy import spiderloader
from twisted.internet import reactor, defer
from multiprocessing import Process, Queue



if __package__ is None or __package__ == '':
    from spiders.default import DefaultSpider
else:
    from .spiders.default import DefaultSpider


class ScraperAPI:
    def __init__(self):
        self.results = []    


    def getSpiderList(self) -> list:
        """Get a list of all spider names in the project

        Returns:
            list: A list of all spider names implemented in this project
        """
        settings = project.get_project_settings()
        spider_loader = spiderloader.SpiderLoader.from_settings(settings)
        spiders = spider_loader.list()

        return spiders

    def getRelevantSpider(self, spiderName: str) -> Type:
        """ Returns the relevant spider type based on a search string

        Args:
            spider (str): search string

        Returns:
            Type: The class type of the relevant Spider
        """
        spiderList = self.getSpiderList()

        # Set relevant spider to Default as a fallback
        relevantSpider = DefaultSpider

        for name in spiderList:
            if (name == spiderName):
                relevantSpider = self.loadSpider(name)

        return relevantSpider

    def loadSpider(self, spiderName) -> Type:
        """ Loads spider with given name

        Args:
            spiderName (_type_): name of spider

        Returns:
            Type: Class type of relevant spider
        """
        settings = project.get_project_settings()
        spider_loader = spiderloader.SpiderLoader.from_settings(settings)
        return (spider_loader.load(spiderName))

    
    def runSpiders(self, scrapeRequestList: list) -> list:
        """ runs a list of spiders and urls

        Args:
            scrapeRequestList (list): List of scrape requests

        Returns:
            list: Results of scraping
        """
        newSpiderList = {}
        newSpiderList['spiderURLList'] = []
        for spiderObject in scrapeRequestList:
            newSpiderList['spiderURLList'].append({
              'spider': self.getRelevantSpider(spiderObject['scraper']),
              'urls' : spiderObject['urls']
            })

        multiThreadQueue = Queue()
        process = Process(target=self.dispatchSpiders, args=(multiThreadQueue, newSpiderList, self.crawlerResults))
        process.start()
        self.results = multiThreadQueue.get()
        process.join()  

        return(json.dumps(self.results))

    
    def dispatchSpiders(self, multiThreadQueue: Queue, spiderURLList: list, resultsCallback: Function) -> Queue:
        """This function will insantiate the crawler runner and add all the relevant spiders/urls from the list

        Args:
            multiThreadQueue (Queue): 
            spiderURLList (list): A list of spiders to be ran and their urls
            resultsCallback (Function): Function that runs once scraped. In this case it is always crawler_results

        Returns:
            Queue: _description_
        """
        try:
            runner = crawler.CrawlerRunner(settings={
                "FEEDS": {
                    "items.json": {
                        "format": "json", 
                        "overwrite": True
                        },

                },
            })
            deferredList = set()
            for spiderURL in spiderURLList['spiderURLList']:
              deferred = runner.crawl(spiderURL['spider'], input=spiderURL['urls'], callback=resultsCallback)
              deferredList.add(deferred)
            defer.DeferredList(deferredList).addBoth(lambda _: reactor.stop())
            reactor.run()
            multiThreadQueue.put(self.results)
        except Exception as e:
            multiThreadQueue.put(e)

        return multiThreadQueue
        
    def crawlerResults(self, data: list) -> None:
        """A callback function that gets passed to spiders when they're queued for execution

        Args:
            data (list): Output data
        """
        [self.results.append(article) for article in data]


# just for debug purposes. Not sure if leaving this here is a code smell. Probably is.
if __name__ == "__main__":
    scraper = ScraperAPI()

    someRequest = [
      {
          "scraper": "www.reuters.com",
          "urls": [
              "https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/",
              "https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/",
              "https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/"
          ],
       },
       {
          "scraper": "default",
          "urls": [
              "https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/",
              "https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/",
              "https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/"
          ],
       },
       {
          "scraper": "inc.com",
          "urls": [
              "https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/",
              "https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/",
              "https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/"
          ],
       },
        {
          "scraper": "denverpost.com",
          "urls": [
              "https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/",
              "https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/",
              "https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/"
          ],
       },
       {
          "scraper": "forbes.com",
          "urls": [
              "https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/",
              "https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/",
              "https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/"
          ],
       },
       {
          "scraper": "marketwatch.com",
          "urls": [
              "https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/",
              "https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/",
              "https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/"
          ],
       },
    ]

    someOtherRequest = [{'scraper': 'reuters', 'urls': ['https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/', 'https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/', 'https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/'], 'create': 'domain_name'}]

    scraper.runSpiders(someOtherRequest)

    response = {}
    response['articles'] = scraper.results
    print(response)