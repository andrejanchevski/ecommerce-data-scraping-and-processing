import scrapy
from ..items import EtsyProductWithFeedbacksMongo
from ..items import EtsyProductReviewsMongo


class EtsyProductFeedbacksSpider(scrapy.Spider):
    name = 'etsy_products_feedbacks_mongo'
    start_urls = ['https://www.etsy.com/c/jewelry-and-accessories?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/clothing-and-shoes?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/home-and-living?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/wedding-and-party?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/toys-and-entertainment?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/art-and-collectibles?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/craft-supplies-and-tools?ref=pagination&page=' + str(i) for i in
                    range(1, 2)] \
                 + ['https://www.etsy.com/c/vintage?ref=pagination&page=' + str(i) for i in range(1, 250)]

    def parse(self, response, **kwargs):
        links = response.css('ul.responsive-listing-grid li  a.listing-link::attr(href)').extract()
        for link in links:
            yield response.follow(str(link), callback=self.parse_product_feedbacks_mongo)

    def parse_product_feedbacks_mongo(self, response):
        productItem = EtsyProductWithFeedbacksMongo()
        categories = []
        productShopName = response.css('#listing-page-cart .wt-text-body-01 .wt-text-link-no-underline span::text') \
            .extract()
        productName = response.css('#listing-page-cart .wt-break-word').xpath('string()').extract()
        shopLink = response.css('#listing-page-cart .wt-text-body-01 .wt-text-link-no-underline::attr(href)').extract()
        productReviews = response.css('#reviews .wt-text-body-03::text').extract()
        productRating = response.css('.review-col span.wt-display-inline-block').xpath(
            "input[@name='rating']/@value").extract()

        productOriginalPrice = response.css('#listing-page-cart .wt-text-strikethrough').xpath('string()').extract()
        productPrice = response.css('#listing-page-cart .wt-mr-xs-2').xpath('string()').extract()

        if len(productOriginalPrice) == 0:
            productOriginalPrice = ""
            productPrice = str(productPrice[0]).strip()
            productPrice = productPrice.replace('+', '')
        else:
            productOriginalPrice = str(productOriginalPrice[0]).strip().split('\n')[1].strip()
            productOriginalPrice = productOriginalPrice.replace('+', '')
            productPrice = str(productPrice[0]).strip().split('\n')[1].strip()

        productItem['productName'] = str(productName[0]).strip()
        productItem['productShopName'] = str(productShopName[0]).strip()
        shopLink = str(shopLink[0]).strip().split("?")[0] if shopLink[0] else ""
        productItem['shopLink'] = shopLink
        productItem['productNoOfReviews'] = str(productReviews[0]).strip().split(" ")[0]
        productItem['productRating'] = productRating[0]
        productItem['productPrice'] = productPrice
        productItem['productOriginalPrice'] = productOriginalPrice

        productItems = []
        productItemsSelect = response.css('#listing-page-cart #inventory-variation-select-0')
        if len(productItemsSelect) != 0:
            productItemsOptions = productItemsSelect.css('option::text').extract()
            for pi in productItemsOptions[1:]:
                productItems.append(str(pi).strip())

        productItem['productItems'] = productItems

        productFeedbacksTabLess = response.css('.listing-info .wt-align-items-flex-start .wt-grid--block')
        productFeedbacksSlots = productFeedbacksTabLess[0].css('.wt-grid__item-xs-12')
        reviews = []
        for productFeedbackSlot in productFeedbacksSlots:
            reviewItem = EtsyProductReviewsMongo()
            productFeedbackReviewer = productFeedbackSlot.css('.wt-text-caption a.wt-text-link::text').extract_first()
            productFeedbackDate = productFeedbackSlot.css('.wt-mb-xs-1 .wt-text-gray::text').extract()
            productFeedbackRating = productFeedbackSlot.css('.wt-flex-md-auto .wt-mb-xs-1 span.wt-mr-xs-1').xpath(
                "input[@name='rating']/@value").extract()
            productFeedbackText = productFeedbackSlot.css('.wt-text-body-01 .wt-break-word').xpath('string()').extract()
            reviewItem['feedbackRating'] = str(productFeedbackRating[0]).split(" ")[0]
            reviewItem['feedbackText'] = str(productFeedbackText[0]).strip() if len(
                productFeedbackText) != 0 else ""
            reviewItem['feedbackReviewer'] = productFeedbackReviewer if productFeedbackReviewer else ""
            productFeedbackDate = productFeedbackDate[0].split()
            reviewItem['feedbackDate'] = "".join(productFeedbackDate[-3:])
            reviews.append(reviewItem)

        productItem['productReviews'] = reviews

        categoriesTags = response.css('#wt-content-toggle-tags-read-more .wt-action-group__item')
        if len(categoriesTags) != 0:
            for ct in categoriesTags:
                categoryLink = ct.css('.wt-btn::attr(href)').extract_first()
                if 'cat_tag' in str(categoryLink):
                    categoryName = ct.css('.wt-btn::text').extract_first()
                    categories.append(str(categoryName).strip())
        productItem['categories'] = categories

        yield productItem
