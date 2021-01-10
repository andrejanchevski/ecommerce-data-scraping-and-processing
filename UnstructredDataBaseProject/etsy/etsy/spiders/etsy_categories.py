import scrapy
from ..items import EtsyCategoryItem


class EtsyShopSpider(scrapy.Spider):
    name = 'etsy_categories'
    start_urls = [
        'https://www.etsy.com/help/categories/seller'
    ]

    def parse(self, response, **kwargs):
        categoryList = response.css('.category-list')
        yield from self.ul_parsing(categoryList, parentCategory="")

    def ul_parsing(self, categoryList, parentCategory):

        listElements = categoryList.xpath('./li')
        for li in listElements:
            items = EtsyCategoryItem()
            categoryName = li.xpath('./span/text()').extract()
            items['categoryName'] = categoryName
            items['parentCategoryName'] = parentCategory
            yield items
            subList = li.xpath('./ul')
            if len(subList) != 0:
                yield from self.ul_parsing(subList, categoryName)
            else:
                continue



