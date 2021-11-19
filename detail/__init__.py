'''
Course type, currency, tuition, schedule
'''
import asyncio
from pprint import pprint
import time
import aiohttp
import bs4

from async_download_parse import fetch_all
from detail.overview import parse_detail_for_one_course
from write_to_json import read_from_json


def read_courses():
    courses = read_from_json('./final_files/course_7755_EUR_XW_1022.json')
    return courses


async def fetch_page(url, session):
    resp = await session.request(method="GET", url=url)
    html = await resp.text()
    page = bs4.BeautifulSoup(html, 'html.parser')
    return page


async def get_details(course, session, no_info_courses):
    url = course['url']
    page = await fetch_page(url, session)
    detail = parse_detail_for_one_course(page, course, no_info_courses)
    return detail


async def chain_up_get_detail():
    courses = read_courses()
    no_info_courses = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for course in courses:
            tasks.append(get_details(course, session, no_info_courses))
        details = await asyncio.gather(*tasks)
    return details, no_info_courses






