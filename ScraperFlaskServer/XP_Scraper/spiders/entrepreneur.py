import scrapy

class MarketwatchSpider(scrapy.Spider):
    name = 'www.entrepreneur.com'

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
        content = response.xpath('/html/body/div/main/div/div[2]/div/article/section/div[3]/div//text()[not (ancestor-or-self::b)]').re(r'[^ ^\n^\t].*[^\t^\n]')
        content = ' '.join(content)
        
        date = response.css('time::attr(datetime)').get()
        date = date.split(' ')[0]
        
        self.parsedData.append({
            'title': response.xpath('/html/body/div/main/div/div[2]/div/article/section/div[1]/h1//text()').re(r'[^ ^\n^\t].*[^\t^\n]')[0],
            'expert': response.xpath('/html/body/div/main/div/div[2]/div/article/section/div[2]/a//text()').re(r'[^ ^\n^\t].*[^\t^\n]')[0],
            'date': date, 
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)