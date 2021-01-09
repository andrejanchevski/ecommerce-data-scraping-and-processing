import scrapy
from ..items import EtsyShopItem


class EtsyShopSpider(scrapy.Spider):
    name = 'etsy_shops'
    start_urls = [
        'https://www.etsy.com/search/shops?page=' + str(i) for i in range(1, 1200)
    ]

    def parse(self, response, **kwargs):
        links = response.css('.wrap a::attr(href)').extract()
        for link in links:
            print(str(link))
            yield response.follow(str(link), callback=self.parse_shop)

    def parse_shop(self, response):
        items = EtsyShopItem()
        shop_name = response.css('.mb-lg-1::text').extract()
        noOfItems = response.css('.wt-mr-md-2::text').extract_first()
        shopOwner = response.css('.img-container p::text').extract()
        shopAddress = response.css('.br-lg-1::text').extract()
        noOfSales = response.css('.no-wrap a::text').extract_first()
        shopImageLink = response.css('.shop-icon-external::attr(src)').extract()
        yearCreated = response.css('.etsy-since::text').extract()

        items['shopName'] = shop_name
        items['noOfItems'] = noOfItems
        items['shopOwner'] = shopOwner
        items['shopAddress'] = shopAddress
        items['noOfSales'] = str(noOfSales).split(' ')[0] if noOfSales is not None else ''
        items['shopImageLink'] = shopImageLink
        items['yearCreated'] = str(yearCreated[0]).split(' ')[3].strip() if yearCreated is not None else ''
        yield items
