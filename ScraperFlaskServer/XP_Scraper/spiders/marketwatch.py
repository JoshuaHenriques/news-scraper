import calendar
import scrapy
from datetime import date as _date

class MarketwatchSpider(scrapy.Spider):
    name = 'www.marketwatch.com'

    def __init__(self, input = None, callback= None):
        super().__init__()
        self.input = input
        self.output_callback = callback
        self.parsedData = []


    def start_requests(self):
        """_summary_

        Yields:
            _type_: _description_
        """
        urls = self.input
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date = response.css('.timestamp--pub::text').re(r'[^ ^\n].*')[0] # 'First Published: March 14, 2022 at 9:40 a.m. ET'
        date = ' '.join(date.split()[2:5]) # March 14, 2022
        
        # If site changes from March to Mar this breaks
        month = list(calendar.month_name).index(date.split()[0])
            
        day = date.split()[1]
        day = day[0:len(day)-1]
            
        year = date.split()[2]
            
        date = _date(int(year), int(month), int(day))
        date = date.strftime("%Y-%m-%d")
        
        content = response.xpath('/html/body/main/div[1]/div[3]//text()').re(r'[^ ^\n].*')
        content = ' '.join(content)
        
        self.parsedData.append({
            'title': response.xpath('/html/body/main/div/div/div/h1//text()').re(r'[^\n].*')[0],
            'expert': response.xpath('/html/body/main/div[1]/div[1]/div[2]/div[2]/div/a/h4//text()').get(),
            'date': date,
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)