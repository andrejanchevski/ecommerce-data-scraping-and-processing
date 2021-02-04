import scrapy
from ..items import EtsyShopWithFeedbacksMongo
from ..items import EtsyShopFeedbacksMongo
import json

class EtsyShopSpider(scrapy.Spider):
    name = 'etsy_shops_feedbacks_mongo'

    def start_requests(self):
        with open('etsy/products_crawled.json') as filehandler:
            products = json.loads(filehandler.read())
        urls = [p['shopLink'] for p in products]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        items = EtsyShopWithFeedbacksMongo()
        shop_name = response.css('.shop-name-and-title-container h1::text').extract_first()
        current_items = response.css('.is-selected .wt-mr-md-2::text').extract_first()
        shop_owner_link = response.css('.shop-owner .img-container a::attr(href)').extract_first()
        shop_owner_name = response.css('.shop-owner .img-container p::text').extract_first()
        shop_address = response.css('.shop-home-header-container .shop-info .shop-location') \
            .xpath('string()').extract_first()
        no_of_sales = response.css('.pt-lg-2 .pt-xs-3:nth-child(1)').xpath('string()').extract_first()
        no_of_admirers = response.css('.pt-lg-2 .pt-xs-3:nth-child(2) a::text').extract_first()
        shop_image_link = response.css('.shop-home-header-container .shop-icon img::attr(src)').extract_first()
        shop_rating = response.css('.shop-home-header-container .shop-sales-reviews .reviews-link-shop-info '
                                   '.wt-mr-xs-1').xpath("input[@name='rating']/@value").extract_first()
        shop_description = response.css('.prose span::text').extract_first()
        print(shop_description)
        year_created = response.css('.shop-home-wider-sections .mb-xs-4 span::text').extract()
        yearCreated = ''
        if len(year_created) == 2:
            yearCreated = year_created[1]

        items['shopName'] = str(shop_name).strip() if shop_name else 'Shop Not Active'
        items['currentItems'] = current_items if current_items else 0
        items['shopOwner'] = str(shop_owner_name).strip() if shop_owner_name else ''
        items['shopOwnerLink'] = 'https://www.etsy.com' + str(shop_owner_link) if shop_owner_link else ''
        items['shopAddress'] = str(shop_address).strip() if shop_address else 'Location Unknown'
        items['currentNoOfAdmirers'] = str(no_of_admirers).split(' ')[0] if no_of_admirers else 0
        items['currentSales'] = str(no_of_sales).split(' ')[0] if no_of_sales else 0
        items['shopImageLink'] = str(shop_image_link).strip() if shop_image_link else ''
        items['yearCreated'] = yearCreated if year_created else ''
        items['shopRating'] = shop_rating if shop_rating else 0
        items['shopDescription'] = shop_description if shop_description else ''

        shopFeedbacks = []
        shopFeedbackSlots = response.css('.reviews-list .review-item')
        for shopFeedbackSlot in shopFeedbackSlots:
            shopFeedbackItem = EtsyShopFeedbacksMongo()
            feedback_reviewer = shopFeedbackSlot.css('.flag-body .shop2-review-attribution a::text').extract_first()
            feedback_reviewer_link = shopFeedbackSlot.css('.flag-body .shop2-review-attribution a::attr(href)') \
                .extract_first()
            feedback_date = shopFeedbackSlot.css('.flag-body .shop2-review-attribution').xpath('string()') \
                .extract_first()
            feedback_rating = shopFeedbackSlot.css('.flag-body .mb-xs-0 .stars-svg') \
                .xpath("input[@name='rating']/@value").extract_first()
            feedback_text = shopFeedbackSlot.css('.text-gray-lighter .prose::text').extract_first()
            feedback_product = shopFeedbackSlot.css('.flag .hide-sm p::text').extract_first()

            shopFeedbackItem['feedbackDate'] = str(feedback_date).strip().split('on')[1].strip() \
                if feedback_date else ''
            shopFeedbackItem['feedbackReviewer'] = feedback_reviewer if feedback_reviewer else 'anonymous '
            shopFeedbackItem['feedbackReviewerUrl'] = feedback_reviewer_link if feedback_reviewer_link else ''
            shopFeedbackItem['feedbackRating'] = feedback_rating if feedback_rating else 0
            shopFeedbackItem['feedbackText'] = str(feedback_text).strip() if feedback_text else ''
            shopFeedbackItem['feedbackForProduct'] = str(feedback_product).strip() if feedback_product else ''
            shopFeedbacks.append(shopFeedbackItem)

        items['shopFeedbacks'] = shopFeedbacks

        yield items
