import scrapy
from ..items import EtsyProducts


class EtsyShopProductsSpider(scrapy.Spider):
    name = 'etsy_products'
    start_urls = ['https://www.etsy.com/c/jewelry-and-accessories?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/clothing-and-shoes?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/home-and-living?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/wedding-and-party?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/toys-and-entertainment?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/art-and-collectibles?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/craft-supplies-and-tools?ref=pagination&page=' + str(i) for i in range(1, 250)] \
                 + ['https://www.etsy.com/c/vintage?ref=pagination&page=' + str(i) for i in range(1, 250)]


    def parse(self, response, **kwargs):
        items = EtsyProducts()
        categoryProduct = response.css('div.body-max-width div.float-left h1::text').extract()
        productCarts = response.css('ul.responsive-listing-grid li')
        for productCart in productCarts:
            productName = productCart.css('h3.text-body').xpath('string()').extract()
            productName = str(productName[0]).strip()
            productShop = productCart.css('.v2-listing-card__shop p.text-gray-lighter::text').extract()
            productRating = productCart.css('.v2-listing-card__rating span.stars-svg')\
                .xpath("input[@name='rating']/@value").extract()
            productReviews = productCart.css('.v2-listing-card__rating span.text-body-smaller::text').extract()
            productPrice = productCart.css('.currency-value::text').extract()
            productPriceOriginal = 0
            productPriceSale = 0
            if len(productPrice) == 2:
                productPriceOriginal = productPrice[1]
                productPriceSale = productPrice[0]
            elif len(productPrice) == 1:
                productPriceOriginal = productPrice[0]

            items['productName'] = productName
            items['productShop'] = productShop
            items['productCategory'] = categoryProduct
            items['productRating'] = productRating
            items['productReviews'] = productReviews
            items['productPriceOriginal'] = productPriceOriginal
            items['productPriceSale'] = productPriceSale

            yield items
