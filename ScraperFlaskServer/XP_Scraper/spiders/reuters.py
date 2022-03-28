import calendar
import scrapy
from datetime import date as _date

class ReutersSpider(scrapy.Spider):
    name = 'www.reuters.com'

    def __init__(self, input = None, callback= None):
        super().__init__()
        self.input = input
        self.output_callback = callback
        self.parsedData = []


    def start_requests(self):
        urls = self.input
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = response.css('.article-body__element__OOj6H::text').getall()
        content = ' '.join(content)
        
        date = response.css('.date-line__date__23Ge-::text').getall()[0]
        
        # If site changes from March to Mar this breaks
        month = list(calendar.month_name).index(date.split()[0])
            
        day = date.split()[1]
        day = day[0:len(day)-1]
            
        year = date.split()[2]
            
        date = _date(int(year), int(month), int(day))
        date = date.strftime("%Y-%m-%d")
        
        self.parsedData.append({
            'title': response.css('.heading__heading_2__3Fcw5::text').get(),
            'expert': response.css('.author-name__author__1gx5k::text').get(),
            'date': date,
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)
