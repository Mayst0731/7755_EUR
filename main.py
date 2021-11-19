'''
Category(url),
Course name(url),
Course type, currency, tuition, schedule(start_time, end_time, duration)
'''

import asyncio
import time


import requests

from category import scrape_category
from course import get_courses
from detail import chain_up_get_detail
from detail.overview import parse_detail_for_one_course
from download_parse import download_page
from format_output import modify_to_en_duration_and_rewrite_1
from weird_courses import add_modified_loc_3, online_live_desc_2, duration_desc_integrate, print_out_all_durations, \
    re_write_duration_info, add_three_new_courses
from write_to_json import write_to_json


def scraper():
    '''
    1. Get executive education category and course urls
    2. Write into Json
    '''
    executive_education_url = "https://www.nyenrode.nl/opleidingen/executive-education"
    categories = scrape_category(executive_education_url)
    categories = category_rename_map(categories)
    write_to_json(categories, 'final_files/category_7755_EUR_XW_1117.json')
    courses = get_courses(categories)
    write_to_json(courses, './final_files/course_7755_EUR_XW_1117.json')


def category_rename_map(categories):
    '''
    Change two categories' name into their corresponding names in database
    '''
    mapping = {"Digitale Transformatie, Innovatie & ICT": "Digitale Transformatie, Innovatie en ICT",
                "Maatwerk en InCompany": "Maatwerk / InCompany",
            }
    for cate in categories:
        if cate["category"] in mapping:
            cate["category"] = mapping.get(cate["category"])
    return categories


def sync_get_details(no_info_courses, sync_no_info_courses):
    '''
    fetch courses which are incomplete
    '''
    session = requests.session()
    details = []
    for course in no_info_courses:
        page = download_page(course['url'], session)
        detail = parse_detail_for_one_course(page, course, sync_no_info_courses)
        details.append(detail)
    return details, sync_no_info_courses


def rewrite_scraped_details(async_details, sync_details):
    '''
    merge details get in both async way and sync way
    '''
    details = async_details+sync_details
    course_dict = dict()
    for detail in details:
        course_dict[detail['name']] = detail
    final_details = []
    for course_name, course_info in course_dict.items():
        final_details.append(course_info)
    return final_details


if __name__ == '__main__':
    scraper()
    start = time.time()
    # chain_up_get_detail in detail folder
    async_details, no_info_courses = asyncio.run(chain_up_get_detail())
    print(f'async no info {len(no_info_courses)}')
    sync_details, sync_no_info_courses = sync_get_details(no_info_courses, [])
    print(len(async_details))
    print(f'sync no info {len(sync_no_info_courses)}')
    final_details = rewrite_scraped_details(async_details, sync_details)
    print(f'the number of courses {len(final_details)}')
    # this is origin details get from course pages
    write_to_json(final_details, 'final_files/comprehensive_detail_7755_EUR_XW_1117.json')

    # below is formatting details
    modify_to_en_duration_and_rewrite_1()
    online_live_desc_2()
    add_modified_loc_3()
    duration_desc_integrate()
    print_out_all_durations()
    re_write_duration_info()
    add_three_new_courses()
    end = time.time()
    diff = end - start
    print(f'using {diff} seconds, {diff / 60} mins')

