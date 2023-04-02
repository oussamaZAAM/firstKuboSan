# import csv
# from bs4 import BeautifulSoup
#
# # Chrome & Firefox
# from selenium import webdriver
#
# # Edge
# # from msedge.selenium_tools import Edge, EdgeOptions
#
# # Start Up the webdriver
# # Chrome & Firefox
# driver = webdriver.Chrome()
#
#
# def get_url(search_term):
#     """Generate a url from search term"""
#     template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
#     search_term = search_term.replace(' ', '+')
#     return template.format(search_term)
#
#
# url = get_url('monogatari')
# print(url)
# driver.get(url)
#
# # Retrieve HTML Text
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# results = soup.find_all('div', {'data-component-type': 's-search-result'})
#
# # Prototype the record
# item = results[0]
# atag = item.h2.a
# description = atag.span.text.strip()
#
# url = 'https://www.amazon.com' + atag.get('href')
#
# price_parent = item.find('span', 'a-price')
# price = price_parent.find('span', 'a-offscreen').text
#
# rating = item.i.text
#
# review_count_parent = item.find('a', 'a-link-normal')
# review_count = item.find('span', 'a-size-base s-underline-text').text
#
#
# # Generalize the pattern
# def extract_record(item):
#     # Description and URL
#     atag = item.h2.a
#     description = atag.span.text.strip()
#     url = 'https://www.amazon.com' + atag.get('href')
#
#     try:
#         # Price
#         price_parent = item.find('span', 'a-price')
#         price = price_parent.find('span', 'a-offscreen').text
#     except AttributeError:
#         return
#
#     try:
#         # Rates
#         rating = item.i.text
#         review_count = item.find('span', 'a-size-base s-underline-text').text
#     except AttributeError:
#         rating = ''
#         review_count = ''
#
#     result = (description, url, price, rating, review_count)
#     return result
#
#
# records = []
# results = soup.find_all('div', {'data-component-type': 's-search-result'})
#
# for item in results:
#     record = extract_record(item)
#     if record:
#         records.append(record)
#
# # Show Prices
# # for row in records:
# #     print(row[2]+': '+row[0])
#
#
# #Navigate to the next page
# def get_url(search_term):
#     """Generate a url from search term"""
#     template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
#     search_term = search_term.replace(' ', '+')
#
#     #Add query to the url
#     url = template.format(search_term)
#
#     #Add url query
#     url += '&page={}'
#     return url


###  Final Result  ###

import csv
from bs4 import BeautifulSoup

def get_url(search_term):
    """Generate a url from search term"""
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(' ', '+')

    #Add query to the url
    url = template.format(search_term)

    #Add url query
    url += '&page={}'
    return url

def extract_record(item):
    # Description and URL
    atag = item.h2.a
    description = atag.span.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        # Price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        # Rates
        rating = item.i.text
        review_count = item.find('span', 'a-size-base s-underline-text').text
    except AttributeError:
        rating = ''
        review_count = ''

    result = (description, url, price, rating, review_count)
    return result

def main(search_term):
    #Startup the webdrier
    from selenium import webdriver
    driver = webdriver.Chrome()

    records =[]
    url = get_url(search_term)

    for page in range(1, 4):
        driver.get(url.format(page))
        # Retrieve HTML Text
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    #Save data to a CSV file
    with open('firstKumoSan.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'URL', 'Price', 'Rating', 'Review Count'])
        writer.writerows(records)

main('Monogatari')