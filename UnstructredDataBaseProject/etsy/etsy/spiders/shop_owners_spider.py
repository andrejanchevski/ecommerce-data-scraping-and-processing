import scrapy
from ..items import EtsyShopOwners
import json

class EtsyShopSpider(scrapy.Spider):
    name = 'etsy_shop_owners_mongo'

    def start_requests(self):
        with open('etsy/shops_crawled.json') as filehandler:
            shops = json.loads(filehandler.read())
        urls = [s['shopOwnerLink'] for s in shops]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        items = EtsyShopOwners()
        shop_owner_name = response.css('.wt-display-inline-flex::text').extract()
        shop_name = response.css('#content .wt-text-center-xs::text').extract_first()
        owner_location = response.css('.wt-nudge-b-1+ span::text').extract_first()
        owner_about_me = response.css('.wt-text-caption #wt-content-toggle-profile-about p::text').extract_first()
        owner_following = 0
        owner_followers = 0
        owner_follow_info = response.css('#content .wt-text-link-no-underline span::text').extract()
        if len(owner_follow_info) > 2:
            owner_following = owner_follow_info[0]
            owner_followers = owner_follow_info[1]
        shopOwnerName = ''
        if len(shop_owner_name) > 0:
            shopOwnerName = str(shop_owner_name[0]).strip()

        items['shopName'] = str(shop_name).strip() if shop_name else ''
        items['shopOwnerName'] = shopOwnerName
        items['ownerFollowing'] = owner_following
        items['ownerFollowers'] = owner_followers
        items['ownerLocation'] = owner_location if owner_location else ''
        items['ownerAboutMe'] = owner_about_me if owner_about_me else ''

        yield items
