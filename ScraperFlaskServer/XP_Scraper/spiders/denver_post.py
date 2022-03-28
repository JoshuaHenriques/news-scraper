import scrapy

class DenverPostSpider(scrapy.Spider):
    name = 'www.denverpost.com'

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
        expert = response.css('.author-name::text').getall()
        expert = ' '.join(expert)
        
        date = response.css('time::attr(datetime)').get()
        date = date.split()[0]
        
        content = response.xpath('/html/body/div/div/div/main/article/div/div/div/div/p//text()').getall()
        content = ' '.join(content)
        
        self.parsedData.append({
            'title': response.xpath('/html/body/div/div/div/main/article/header/div/div/div/h1/span//text()').re(r'[^ ^\n^\t].*[^\t]')[0],
            'expert': expert,
            'date': date,
            'content': content,
            'url': response.url,
        })
        yield self.parsedData

    def close(self, spider, reason):
        self.output_callback(self.parsedData)
