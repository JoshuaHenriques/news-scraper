import calendar
import scrapy
from datetime import date as _date

class MarketwatchSpider(scrapy.Spider):
    name = 'www.forbes.com'

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
            
            # Trouble type site:
            # https://www.forbes.com/sites/javierpaz/2022/03/16/the-best-global-crypto-exchanges/?sh=5b4aca7d742c
            # Working type sites:
            # https://www.forbes.com/sites/jamiecartereurope/2022/03/15/asteroid-the-size-of-a-grand-piano-strikes-earth-and-we-knew-exactly-where-and-when-says-nasa/?sh=79130c5e3637
            
    def parse(self, response):
        content = response.xpath('/html/body/div/article[1]/main/div[2]/div[2]/div//text()[not (ancestor-or-self::script or ancestor-or-self::noscript)]').re(r'[^ ^\n].*')
        content = ' '.join(content)
        
        date = response.xpath('/html/body/div/article/main/div[2]/div[2]/div[1]/div/div/div/time//text()').get()
        date = date[:len(date) - 1]
        
        # If site changes from Mar to March this breaks
        month = list(calendar.month_abbr).index(date.split()[0])
            
        day = date.split()[1]
        day = day[0:len(day)-1]
        
        year = date.split()[2]
        
        date = _date(int(year), int(month), int(day))
        date = date.strftime("%Y-%m-%d")
        
        self.parsedData.append({
            'title': response.css('.fs-headline::text').get(),
            # Works for some pages
            'expert': response.xpath('/html/body/div/article[1]/main/div[2]/div[2]/div[2]/div/div[1]/div/div/div[1]/span/a//text()').get(),
            'date': date, 
            # Works for some pages
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)