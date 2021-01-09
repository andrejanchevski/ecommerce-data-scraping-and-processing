import scrapy
from ..items import EtsyShopOwners


class EtsyShopSpider(scrapy.Spider):
    name = 'etsy_shop_owners'
    start_urls = [
        'https://www.etsy.com/search/shops?page=' + str(i) for i in range(1, 1200)
    ]

    def parse(self, response, **kwargs):
        links = response.css('.real-name a::attr(href)').extract()
        for link in links:
            yield response.follow(str(link), callback=self.parse_shop_owner)

    def parse_shop_owner(self, response):
        items = EtsyShopOwners()
        shopName = response.css('#content .wt-text-center-xs::text').extract()
        shopOwnerName = response.css('.wt-display-inline-flex::text').extract()
        ownerFollowInfo = response.css('#content .wt-grid .wt-text-link-no-underline span::text').extract()
        ownerLocation = response.css('.wt-nudge-b-1+ span::text').extract()
        items['shopName'] = shopName
        items['shopOwnerName'] = str(shopOwnerName[0]).strip()
        items['ownerFollowing'] = ownerFollowInfo[0]
        items['ownerFollowers'] = ownerFollowInfo[1]
        items['ownerLocation'] = ownerLocation
        yield items








        yield items
