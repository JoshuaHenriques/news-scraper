import calendar
import scrapy
from datetime import date as _date

class MarketwatchSpider(scrapy.Spider):
    name = 'www.inc.com'

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
        content = response.xpath('/html/body/div/div/div/div/div/div/div/article/article//div//div//text()').re(r'[^ ^\n^\r].*')
        content = ' '.join(content)
        
        date = response.css('.ArticlePubdate__pubdate__3kWwF::text').get()
        
        # If site changes from March to Mar this breaks
        if len(date) <= 13:
            month = list(calendar.month_abbr).index(date.split()[0])
                
            day = date.split()[1]
            day = day[0:len(day)-1]
                
            year = date.split()[2]
            
            date = _date(int(year), int(month), int(day))
            date = date.strftime("%Y-%m-%d")
        else:
            date = 'No date given'
        
        self.parsedData.append({
            'title': response.css('.sc-AxirZ::text').get(),
            'expert': response.css('.sc-fzoyAV a::text').get(),
            'date': date,
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)