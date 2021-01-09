import scrapy
from ..items import EtsyShopFeedbacks


class EtsyShopFeedbackSpider(scrapy.Spider):
    name = 'etsy_feedbacks_shops'
    start_urls = [
        'https://www.etsy.com/search/shops?page=' + str(i) for i in range(1, 300)
    ]

    def parse(self, response, **kwargs):
        links = response.css('.wrap a::attr(href)').extract()
        for link in links:
            print(str(link))
            yield response.follow(str(link), callback=self.parse_shop_feedbacks)

    def parse_shop_feedbacks(self, response):
        items = EtsyShopFeedbacks()

        shopName = response.css('.mb-lg-1::text').extract()
        feedback = response.css('div.review-item .m-xs-0').xpath('string()').extract()
        feedbackMetaData = response.css('.shop2-review-attribution').xpath('string()').extract()
        feedbackForProduct = response.css('#reviews .hide-sm p::text').extract()
        feedbackGrade = response.css('div.review-item span.stars-svg').xpath("input[@name='rating']/@value").extract()
        i = 0
        for string in feedbackMetaData:
            temp = str(string).strip()
            feedbackMetaData[i] = temp
            i += 1
        for i in range(0, len(feedback)):
            items['shopName'] = shopName
            items['feedbackGrade'] = feedbackGrade[i]
            items['feedbackForProduct'] = feedbackForProduct[i]
            items['feedback'] = feedback[i]
            splitted = str(feedbackMetaData[i]).split(' on ')
            items['reviewer'] = splitted[0].strip()
            items['feedbackDate'] = splitted[1].strip()
            yield items
