from scrapy import Spider, Request
from bubbletea.items import BubbleteaItem
import re


class bubbletea(Spider):
    name = 'bubbletea_spider'
    start_urls = ['https://www.yelp.com/search?find_desc=Bubble%20Tea&find_loc=New%20York']
    allowed_urls = ['https://www.yelp.com/']


    def parse(self, response):
        pg_num = response.xpath('//span[@class=" text__09f24__2tZKC text-color--black-extra-light__09f24__38DtK text-align--left__09f24__3Drs0"]/text()').extract_first()
        pg_num = int(re.findall('\d+', pg_num)[-1])

 
        url_list = [f'https://www.yelp.com/search?find_desc=Bubble%20Tea&find_loc=New%20York&start={(i-1)*10}'
                    for i in range(pg_num)]
         
        
        for url in url_list[:2]:
            print('='*55)
            print(url)
            print('='*55)

            yield Request(url = url, callback = self.parse_pages)


    def parse_result_page(self, response):
        


    # def parse_result_page(self, response):
    #     result = response.xpath('//div[lemon--div__09f24__1mboc border-color--default__09f24__R1nRO]').extract

    #     products = response.xpath('//h4[@class="sku-header"]/a/@href').extract()
    #     product_urls = [f'https://www.bestbuy.com{url}' for url in products]
    #     for url in product_urls[:2]:
    #         # print('='*55)
    #         # print(url)
    #         # print('='*55)
    #         yield Request(url=url, callback=self.parse_product_page)
