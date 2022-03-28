import scrapy

class DefaultSpider(scrapy.Spider):
    name = 'default'
    
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
        content = response.xpath("//body//text()[not (ancestor-or-self::script or ancestor-or-self::noscript or ancestor-or-self::style or ancestor-or-self::button or ancestor-or-self::img or ancestor-or-self::svg)]").re(r'[^ ^\n].*')
        content = ' '.join(content)
        self.parsedData.append({ 
            'content': content,
            'url': response.url,
            })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)
