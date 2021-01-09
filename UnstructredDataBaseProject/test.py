start_urls = ['https://www.etsy.com/c/jewelry-and-accessories?ref=pagination&page=' + str(i) for i in range(1, 2)] \
             + ['https://www.etsy.com/c/clothing-and-shoes?ref=pagination&page=' + str(i) for i in range(1, 4)] \
             + ['https://www.etsy.com/c/home-and-living?ref=pagination&page=' + str(i) for i in range(1, 2)] \
             + ['https://www.etsy.com/c/wedding-and-party?ref=pagination&page=' + str(i) for i in range(1, 2)] \
             + ['https://www.etsy.com/c/toys-and-entertainment?ref=pagination&page=' + str(i) for i in range(1, 2)] \
             + ['https://www.etsy.com/c/art-and-collectibles?ref=pagination&page=' + str(i) for i in range(1, 2)] \
             + ['https://www.etsy.com/c/craft-supplies-and-tools?ref=pagination&page=' + str(i) for i in range(1, 2)] \
             + ['https://www.etsy.com/c/vintage?ref=pagination&page=' + str(i) for i in range(1, 2)]

print(start_urls )