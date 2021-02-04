from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://andrejanchevski:nebidimrdnat123@etsydatacluster.n41nn.mongodb.net/etsydata?retryWrites=true&w=majority")
db = client.etsydata
products = db.products
with open('products_preprocessed.json', encoding='utf8') as filehandler:
    productData = json.load(filehandler)
products.insert_many(productData)
shop_owners = db.shop_owners
with open('shop_owners_crawled.json', encoding='utf8') as filehandler:
    shopOwnersData = json.load(filehandler)
shop_owners.insert_many(shopOwnersData)
categories = db.categories
with open('categories_crawled.json', encoding='utf-8') as filehandler:
    categoryData = json.load(filehandler)
categories.insert_many(categoryData)
shops = db.shops
with open('shops_preprocessed.json', encoding='utf-8') as filehandler:
    shopsData = json.load(filehandler)
shops.insert_many(shopsData)