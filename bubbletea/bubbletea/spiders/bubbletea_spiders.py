from scrapy import Spider, Request
from bubbletea.items import BubbleteaItem
import pandas as pd
import re


class bubbletea(Spider):
    name = 'bubbletea_spider'
    start_urls = [
    'https://www.yelp.com/search?find_desc=Bubble%20Tea&find_loc=New%20York'
    # 'https://www.yelp.com/search?find_desc=bubble%20tea&find_loc=San%20Francisco'
    #'https://www.yelp.com/search?find_desc=bubble%20tea&find_loc=Los%20Angeles'
    ]
    allowed_urls = ['https://www.yelp.com/']

    def start_requests(self):
      # with open('TopCities.txt', 'rb') as cities:
        
        cities = pd.read_csv('TopCities.csv')
        cities = cities['name'][6:7].values.tolist()

        print('='*55)
        print(cities)
        print('='*55)


        for url in cities:
            urls = url.replace(' ','%20')
            urls = 'https://www.yelp.com/search?find_desc=Bubble%20Tea&find_loc='+urls
            yield Request(url = urls, callback = self.parse)


    def parse(self, response):
        try:
            pg_num = response.xpath('//span[@class=" text__09f24__2tZKC text-color--black-extra-light__09f24__38DtK text-align--left__09f24__3Drs0"]/text()').extract_first()
            pg_num = int(re.findall('\d+', pg_num)[-1])
        except:
            print('*****page number issue*****')
            print(pg_num)
            print(f'Offending URL: {response.url}')
            pass

        url_list = [response.url + f'&start={i*10}' for i in range(pg_num)]
        # print('='*55)
        # print(url_list)
        # print('='*55)
        
        for url in url_list:
            yield Request(url = url, callback = self.parse_result_page)


    def parse_result_page(self, response):
        rest_url = response.xpath('//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@href').extract()
        rest_url = list(filter(lambda url: url.find("ad_business_id") == -1, rest_url))
        rest_url = [f'https://www.yelp.com/{url}' for url in rest_url]

        # for places in restaurants:
        #     print('='*55)
        #     print(places)
        #     print('='*55)
        for url in rest_url:
            # print('='*55)
            # print(url)
            # print('='*55)
            
            yield Request(url=url, callback=self.pars_restaurant_page)

    def pars_restaurant_page(self,response):
        business_name = response.xpath('//h1[@class ="lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy"]/text()').extract()
        try:
            rating = response.xpath('//div[@class = "lemon--div__373c0__1mboc arrange__373c0__2C9bH gutter-1-5__373c0__2vL-3 vertical-align-middle__373c0__1SDTo margin-b1__373c0__1khoT border-color--default__373c0__3-ifU"]//span/div/@aria-label').extract()[0]
            rating = int(re.findall('\d+', rating)[0])
        except:
            print('*****no reviews*****')
            print(f'Offending URL: {response.url}')
            rating = None


        try:
            review_num = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT border-color--default__373c0__3-ifU nowrap__373c0__35McF"]/p/text()').extract()[0] 
            review_num = int(re.findall('\d+', review_num)[0])
        
        except:
            print('*****no review numbers!*****')
            print(f'Offending URL: {response.url}')
            review_num = None

        try:
            food_tags = response.xpath('//span[@class = "lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa- text-size--large__373c0__3t60B"]/a/text()').extract()
            food_tags = '/'.join(food_tags)
        except:
            print('*****no tags!!*****')
            print(f'Offending URL: {response.url}')
            food_tags = None        

        try:
            address =  response.xpath('//address[@class ="lemon--address__373c0__2sPac"]//span/text()').extract()
            street = address[0]
            city = address[-1].split(',')[0]
            state = re.findall('[A-Z]+', address[-1].split(',')[1])[0]
            zip5 = re.findall('\d+', address[-1].split(',')[1])[0]
        except:
            print('*****Address issue!!*****')
            print(f'Offending URL: {response.url}')
            address = None   
            street = None
            city = None
            state = None
            Zip5 = None

        
        try:
            domain, latter = response.url.split('=')
            latter = '=bubble%20tea&sort_by=date_asc'
            first_review_url = domain + latter
        except:
            print('*****domain format issue!!*****')
            print(f'Offending URL: {response.url}')
            pass

        meta = {'business_name': business_name, 'rating': rating, 'review_num': review_num, 'food_tags': food_tags,
                'address': address, 'street': street, 'city': city, 'state': state, 'zip5': zip5}

        # print('*'*55)
        # print(first_review_url)        
        # print('*'*55)
        
        yield Request(url=first_review_url, callback=self.parse_first_review, meta = meta)


    def parse_first_review(self, response):
        try:
            first_review_date = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-"]/text()').extract()[0]
        except:
            print('*****No first reviews :( *****')
            print(f'Offending URL: {response.url}')
            first_review_date = None
        
        last_review_url = response.url.replace('asc', 'desc')
        meta = response.meta
        meta['first_review_date'] = first_review_date

        yield Request(url=last_review_url, callback=self.parse_last_review, meta = meta)

    def parse_last_review(self, response):
        try:
            last_review_date = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-"]/text()').extract()[0]
        except:
            print('*****No last reviews :( *****')
            print(f'Offending URL: {response.url}')
            last_review_date = None
        # print('*'*55)
        # print(response.meta['business_name'][0])
        # print(response.meta['address'])
        # print(response.meta['first_review_date'])
        # print(last_review_date)
        # print('*'*55)

        item = BubbleteaItem()             
        item['business_name'] = response.meta['business_name']
        item['rating'] = response.meta['rating']
        item['review_num'] = response.meta['review_num']
        item['food_tags'] = response.meta['food_tags']
        item['address'] = response.meta['address']
        item['street'] = response.meta['street']
        item['city'] = response.meta['city']
        item['state'] = response.meta['state']
        item['zip5'] = response.meta['zip5']
        item['first_review_date'] = response.meta['first_review_date']
        item['last_review_date'] = last_review_date

        yield item







