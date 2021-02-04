# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EtsyShopItem(scrapy.Item):
    # define the fields for your item here like:
    shopName = scrapy.Field()
    noOfItems = scrapy.Field()
    shopOwner = scrapy.Field()
    shopAddress = scrapy.Field()
    noOfSales = scrapy.Field()
    shopImageLink = scrapy.Field()
    yearCreated = scrapy.Field()


class EtsyShopFeedbacks(scrapy.Item):
    shopName = scrapy.Field()
    reviewer = scrapy.Field()
    feedbackDate = scrapy.Field()
    feedback = scrapy.Field()
    feedbackGrade = scrapy.Field()
    feedbackForProduct = scrapy.Field()


class EtsyProducts(scrapy.Item):
    productName = scrapy.Field()
    productCategory = scrapy.Field()
    productRating = scrapy.Field()
    productReviews = scrapy.Field()
    productPriceSale = scrapy.Field()
    productPriceOriginal = scrapy.Field()
    productShop = scrapy.Field()


class EtsyProductFeedbacks(scrapy.Item):
    productName = scrapy.Field()
    productFeedbackRating = scrapy.Field()
    productFeedbackText = scrapy.Field()
    productFeedbackReviewer = scrapy.Field()
    productFeedbackDate = scrapy.Field()


class EtsyShopOwners(scrapy.Item):
    shopName = scrapy.Field()
    shopOwnerName = scrapy.Field()
    ownerFollowers = scrapy.Field()
    ownerFollowing = scrapy.Field()
    ownerLocation = scrapy.Field()
    ownerAboutMe = scrapy.Field()


class EtsyCategoryItem(scrapy.Item):
    categoryName = scrapy.Field()
    parentCategoryName = scrapy.Field()


class EtsyProductWithFeedbacksMongo(scrapy.Item):
    productName = scrapy.Field()
    productShopName = scrapy.Field()
    shopLink = scrapy.Field()
    productNoOfReviews = scrapy.Field()
    productRating = scrapy.Field()
    productPrice = scrapy.Field()
    productOriginalPrice = scrapy.Field()
    productReviews = scrapy.Field()
    productItems = scrapy.Field()
    categories = scrapy.Field()


class EtsyProductReviewsMongo(scrapy.Item):
    feedbackRating = scrapy.Field()
    feedbackText = scrapy.Field()
    feedbackReviewer = scrapy.Field()
    feedbackDate = scrapy.Field()


class EtsyShopWithFeedbacksMongo(scrapy.Item):
    shopName = scrapy.Field()
    currentItems = scrapy.Field()
    shopOwner = scrapy.Field()
    shopOwnerLink = scrapy.Field()
    shopImageLink = scrapy.Field()
    shopRating = scrapy.Field()
    yearCreated = scrapy.Field()
    shopAddress = scrapy.Field()
    currentSales = scrapy.Field()
    currentNoOfAdmirers = scrapy.Field()
    shopDescription = scrapy.Field()
    shopFeedbacks = scrapy.Field()


class EtsyShopFeedbacksMongo(scrapy.Item):
    feedbackReviewer = scrapy.Field()
    feedbackDate = scrapy.Field()
    feedbackText = scrapy.Field()
    feedbackRating = scrapy.Field()
    feedbackForProduct = scrapy.Field()
    feedbackReviewerUrl = scrapy.Field()
