'''
Category(url),
'''
from pprint import pprint

import requests
import urllib.parse

from download_parse import download_page


def scrape_category(start_url):
    session = requests.session()
    page = download_page(start_url, session)
    categories = get_executive_and_other_cates(page,start_url)
    session.close()
    return categories


def get_executive_and_other_cates(page,parent_url):
    cates_sessions = page.find('div', attrs={"data-sf-element": "Row"}).find_all("a", attrs={"target": "_self"})
    categories = []
    for cate_session in cates_sessions:
        name = cate_session.text.strip()
        link = cate_session.get('href')
        url = urllib.parse.urljoin("https://www.nyenrode.nl/opleidingen/executive-education", link)
        category = {"category": name,
                    "url": url,
                    "parent_url": parent_url}
        categories.append(category)
    hard_code_cates = hard_code_other_cates()
    categories += hard_code_cates
    pprint(categories)
    return categories


def hard_code_other_cates():
    mba_url = "https://www.nyenrode.nl/opleidingen/mba"
    master_url = "https://www.nyenrode.nl/opleidingen/master"
    bachelor_url = "https://www.nyenrode.nl/opleidingen/bachelor"
    mba_cate = package_other_cates(mba_url)
    master_cate = package_other_cates(master_url)
    bachelor_cate = package_other_cates(bachelor_url)
    cates = [mba_cate,master_cate, bachelor_cate]
    return cates


def package_other_cates(url):
    if url.endswith("mba"):
        category = "MBAs"
    elif url.endswith("master"):
        category = "Masters"
    elif url.endswith("bachelor"):
        category = "Bachelors"
    parent_url = "https://www.nyenrode.nl/opleidingen/"
    cate = {"category": category,
            "url": url,
            "parent_url": parent_url}
    return cate
