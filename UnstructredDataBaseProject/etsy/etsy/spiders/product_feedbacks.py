import scrapy
from ..items import EtsyProductFeedbacks


class EtsyProductFeedbacksSpider(scrapy.Spider):
    name = 'etsy_product_feedbacks'
    start_urls = ['https://www.etsy.com/c/jewelry-and-accessories?ref=pagination&page=' + str(i) for i in range(1, 2)] \
                 + ['https://www.etsy.com/c/clothing-and-shoes?ref=pagination&page=' + str(i) for i in range(1, 2)] \
                 + ['https://www.etsy.com/c/home-and-living?ref=pagination&page=' + str(i) for i in range(1, 15)] \
                 + ['https://www.etsy.com/c/wedding-and-party?ref=pagination&page=' + str(i) for i in range(1, 2)] \
                 + ['https://www.etsy.com/c/toys-and-entertainment?ref=pagination&page=' + str(i) for i in range(1, 2)] \
                 + ['https://www.etsy.com/c/art-and-collectibles?ref=pagination&page=' + str(i) for i in range(1, 2)] \
                 + ['https://www.etsy.com/c/craft-supplies-and-tools?ref=pagination&page=' + str(i) for i in range(1, 2)] \
                 + ['https://www.etsy.com/c/vintage?ref=pagination&page=' + str(i) for i in range(1, 2)]


    def parse(self, response, **kwargs):
        links = response.css('ul.responsive-listing-grid li  a.listing-link::attr(href)').extract()
        for link in links:
            yield response.follow(str(link), callback=self.parse_product_feedbacks)

    def parse_product_feedbacks(self, response):
        items = EtsyProductFeedbacks()
        productName = response.css('#listing-page-cart .wt-break-word::text').extract()
        productName = str(productName[0]).strip()
        productFeedbacksTabLess = response.css('.listing-info .wt-align-items-flex-start .wt-grid--block')
        productFeedbacksSlots = productFeedbacksTabLess[0].css('.wt-grid__item-xs-12')
        for productFeedbackSlot in productFeedbacksSlots:
            productFeedbackReviewer = productFeedbackSlot.css('.wt-text-caption a.wt-text-link::text').extract()
            productFeedbackDate = productFeedbackSlot.css('.wt-mb-xs-1 .wt-text-gray::text').extract()
            productFeedbackRating = productFeedbackSlot.css('.wt-flex-md-auto .wt-mb-xs-1 '
                                                            'span.wt-mr-xs-1 span.wt-screen-reader-only::text').extract()
            productFeedbackText = productFeedbackSlot.css('.wt-text-body-01 .wt-break-word').xpath('string()').extract()
            items["productName"] = productName
            items["productFeedbackRating"] = str(productFeedbackRating[0]).split(" ")[0]
            items["productFeedbackText"] = str(productFeedbackText[0]).strip()
            items["productFeedbackReviewer"] = productFeedbackReviewer
            if str(productFeedbackDate[0]).startswith("Reviewed"):
                productFeedbackDate = str(productFeedbackDate).split("inactive")[2].strip()
                items["productFeedbackDate"] = productFeedbackDate
            else:
                items["productFeedbackDate"] = str(productFeedbackDate[0]).strip()

            yield items