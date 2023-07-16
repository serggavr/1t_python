
import time
import requests
from bs4 import BeautifulSoup as bs
from random import randint
import csv

URL_TEMPLATE = 'https://books.toscrape.com/catalogue/page-50.html'
booksArr = []

print('start parsing')
def parse_books_site(books_arr, next_page_url, URL_TEMPLATE):
    r = requests.get(next_page_url, timeout=30)
    time.sleep(2)
    soup = bs(r.text, 'html.parser')
    if soup.find('li', class_='next'):
        button_next_url = soup.find('li', class_='next').find('a')['href'].replace('catalogue/', '')
        print(button_next_url)
    else:
        button_next_url = None
    books_page = soup.find_all('article', class_='product_pod')

    def parse_book_pages(books_arr, books_page):
        for bookHtml in books_page:
            time.sleep(2)
            book = {}
            book_page_url = 'https://books.toscrape.com/catalogue/' + bookHtml.find('h3').find('a')['href'].replace('catalogue/', '')
            request = requests.get(book_page_url, timeout=randint(30, 60))
            book_page = bs(request.text, 'html.parser')
            book['book_title'] = book_page.find('h1').get_text()
            book['book_genre'] = book_page.find('ul', class_='breadcrumb').find_all('li')[-2].find('a').get_text()
            book['book_img'] = 'https://books.toscrape.com/' + book_page.find('div', class_='item active').find('img')['src'][6:]
            book['book_rating'] = book_page.find('p', class_='star-rating')['class'][1]
            if book_page.find('div', class_='sub-header').find_next_siblings('p'):
                book['book_description'] = book_page.find('div', class_='sub-header').find_next_siblings('p')[
                    0].get_text().encode("utf-8", "ignore")
            else:
                book['book_description'] = ''
            book_t_body = book_page.find('table', class_='table')
            book['book_upc'] = book_t_body.find('th', string='UPC').find_next_siblings('td')[0].get_text()
            book['book_price_excl_tax'] = book_t_body.find('th', string='Price (excl. tax)').find_next_siblings('td')[
                                              0].get_text()[2:]
            book['book_price_incl_tax'] = book_t_body.find('th', string='Price (incl. tax)').find_next_siblings('td')[
                                              0].get_text()[2:]
            book['book_tax'] = book_t_body.find('th', string='Tax').find_next_siblings('td')[0].get_text()[2:]
            book['book_available'] = ''.join(x for x in book_t_body.find('th', string='Availability').find_next_siblings('td')[0].get_text() if x.isdigit())
            book['book_number_of_reviews'] = book_t_body.find('th', string='Number of reviews').find_next_siblings('td')[0].get_text()
            books_arr.append(book)
        return books_arr
    parse_book_pages(books_arr, books_page)

    if button_next_url is not None:
        return parse_books_site(books_arr, 'https://books.toscrape.com/catalogue/' + button_next_url, URL_TEMPLATE)
    else:
        return books_arr


to_csv = parse_books_site(booksArr, URL_TEMPLATE, URL_TEMPLATE)
file = open('./tmp/parsedData.csv', 'w', newline='')
with file:
    headers = to_csv[0].keys()
    writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")
    writer.writeheader()
    for row in to_csv:
        writer.writerow(row)


print('end parsing')
