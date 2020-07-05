from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def parseurl(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return (soup)


def parsebooksurl(url):
    soup = parseurl(url)
    return (
        ["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in
         soup.findAll("article", class_="product_pod")])


def get_bookspageurls():
    pages_urls = [main_url]
    soup = parseurl(pages_urls[0])
    while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
        new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get(
            "href")
        pages_urls.append(new_url)
        soup = parseurl(new_url)

    bookspageurl = []
    for page in pages_urls:
        bookspageurl.extend(parsebooksurl(page))
    return (bookspageurl)


def get_product_values(url):
    names = []
    prices = []
    stock = []
    img_urls = []
    categories = []
    categories_url = []
    ratings = []

    bookspageurl = get_bookspageurls()

    for url in bookspageurl:
        soup = parseurl(url)
        # product name
        names.append(soup.find("div", class_=re.compile("product_main")).h1.text)
        # product price
        prices.append(soup.find("p", class_="price_color").text[2:])  # get rid of the pound sign
        # product stock availability
        stock.append(soup.find("p", class_="instock availability").text.strip())
        # product image url
        img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))
        # product category
        categories.append(soup.find("a", href=re.compile("../category/books/")).get("href").split("/")[3])
        # product category url
        categories_url.append(
            soup.find("a", href=re.compile("../category/books/")).get("href").replace('..', main_url + 'catalogue'))
        # product rating
        ratings.append(soup.find("p", class_=re.compile("star-rating")).get("class")[1])

    scraped_df = pd.DataFrame(
        {'name': names, "url_img": img_urls, "rating": ratings, 'price': prices, 'stock': stock,
         "product_category": categories, "category_url": categories_url})

    return (scraped_df)


def csv_export(df_data):
    df_data.to_csv(r'prakashbalraj/books_scrape_data.csv', index=False, header=True)
    return ('Successfully data exported to csv!')


if __name__ == '__main__':
    try:
        main_url = "http://books.toscrape.com/"
        output_data = get_product_values(main_url)
        data_export = csv_export(output_data)
    except Exception as err:
        raise ValueError(err)
