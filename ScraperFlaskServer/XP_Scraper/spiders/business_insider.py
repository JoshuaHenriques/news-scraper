import scrapy

class BusinessInsiderSpider(scrapy.Spider):
    name = 'www.businessinsider.com'

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
        content = response.xpath('//html//body//section//section//section//section//section//div//article//div//section//div//div//div//p//text()').re(r'[^ ^\n^\\xa0].*[^\\xa0]')
        content = ' '.join(content)
        
        date = response.css('.byline-timestamp::attr(data-timestamp)').get()
        date = date.split('T')[0]
        
        self.parsedData.append({
            'title': response.css('.post-headline::text').get(),
            'expert': response.css('.byline-author-name::text').get(),
            'date': date,
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)