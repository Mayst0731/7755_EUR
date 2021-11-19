import requests
import bs4


def download_page(url, session):
    source = session.get(url)
    page = source.content
    page = bs4.BeautifulSoup(page, 'html.parser')
    return page
