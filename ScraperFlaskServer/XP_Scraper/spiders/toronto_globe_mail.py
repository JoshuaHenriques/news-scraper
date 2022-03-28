import scrapy

class MarketwatchSpider(scrapy.Spider):
    name = 'www.theglobeandmail.com'

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
        date = response.css('time::attr(datetime)').get()
        date = date.split('T')[0]
        
        content = response.xpath('/html/body/div/main/div[1]/div/div[2]/article//text()').getall()
        content = ' '.join(content)
        
        self.parsedData.append({
            'title': response.xpath('/html/body/div/main/div[1]/div/div[1]/header/div/h1//text()').get(),
            # Can be excluded in some sites or replaced with 'Toronto'
            'expert': response.xpath('/html/body/div/main/div[1]/div/div[2]/div[1]/div/div/div[1]//text()').get(),
            'date': date, 
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)