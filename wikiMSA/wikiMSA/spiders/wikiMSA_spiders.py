from scrapy import Spider, Request
from bestbuy.items import BestbuyItem

class WikiMSASpider(Spider):
    name = 'bestbuy_spider'
    start_urls = ['https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?id=pcmcat247400050000']
    allowed_urls = ['https://www.bestbuy.com']


    def parse(self, response):
        num_pages = int(response.xpath('//ol[@class="paging-list"]/li')[-1].xpath('./a/text()').extract_first())

        url_list = [f'https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?cp={i+1}&id=pcmcat247400050000'
                    for i in range(num_pages)]

        for url in url_list[:2]:
            # print('='*55)
            # print(url)
            # print('='*55)

            yield Request(url = url, callback = self.parse_result_page)

