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

 
        url_list = [f'https://www.yelp.com/search?find_desc=Bubble%20Tea&find_loc=New%20York&start={i*10}'
                    for i in range(pg_num)]

        
        for url in url_list[:2]:
            yield Request(url = url, callback = self.parse_result_page)


    def parse_result_page(self, response):
        # restaurants = response.xpath('//ul[@class=" undefined list__09f24__17TsU"]/li//h4/span/a/text()').extract()[1:]
        # rest_url = ['https://www.yelp.com/biz/' + res.replace(' ', '-') + '-new-york?osq=Bubble+Tea' for res in restaurants]
        rest_url = response.xpath('//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@href').extract()
        rest_url = list(filter(lambda url: url.find("ad_business_id") == -1, rest_url))
        rest_url = [f'https://www.yelp.com/{url}' for url in rest_url]

        # for places in restaurants:
        #     print('='*55)
        #     print(places)
        #     print('='*55)
        for url in rest_url[:2]:
            # print('='*55)
            # print(url)
            # print('='*55)
            
            yield Request(url=url, callback=self.pars_restaurant_page)

    def pars_restaurant_page(self,response):
        business_name = response.xpath('//h1[@class ="lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy"]/text()').extract()
        
        rating = response.xpath('//div[@class = "lemon--div__373c0__1mboc arrange__373c0__2C9bH gutter-1-5__373c0__2vL-3 vertical-align-middle__373c0__1SDTo margin-b1__373c0__1khoT border-color--default__373c0__3-ifU"]//span/div/@aria-label').extract()[0]
        rating = int(re.findall('\d+', rating)[0])
        review_num = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT border-color--default__373c0__3-ifU nowrap__373c0__35McF"]/p/text()').extract()[0] 
        review_num = int(re.findall('\d+', review_num)[0])
        food_tags = response.xpath('//span[@class = "lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa- text-size--large__373c0__3t60B"]/a/text()').extract()
        food_tags = '/'.join(food_tags)
        address =  response.xpath('//address[@class ="lemon--address__373c0__2sPac"]//span/text()').extract()
        street = address[0]
        city = address[1].split(',')[0]
        state = re.findall('[A-Z]+', address[1].split(',')[1])[0]
        zip5 = int(re.findall('\d+', address[1].split(',')[1])[0])

        print('*'*55)
        print(food_tags)
        print(street)
        print(city)
        print(state)
        print(zip5)
        

        print('*'*55)
        













