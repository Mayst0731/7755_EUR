'''
Course name(url)
'''
import collections
from pprint import pprint

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_courses(categories):
    courses = []
    browser = webdriver.Chrome(ChromeDriverManager().install())
    for category in categories:
        get_one_cate_courses(category['category'], category['url'], courses, browser)
    browser.close()
    cleansed_course = clean_repeating_courses(courses)
    return cleansed_course


def get_one_cate_courses(category, url, courses, browser):
    browser.get(url)
    has_next_page_button = True
    while has_next_page_button:
        course_items = browser.find_elements_by_class_name('program-item')
        for course_item in course_items:
            course_url = course_item.find_element_by_tag_name('a').get_property('href')
            course_name = course_item.find_element_by_css_selector('span[class="h4 heading"]').text
            course = {'name': course_name,
                      'url': course_url,
                      'category': [category]}
            courses.append(course)
        try:
            has_next_page_button = browser.find_element_by_css_selector('i[class="fas fa-angle-right"]')
            has_next_page_button.click()
        except:
            break


def clean_repeating_courses(courses):
    cleansed_courses_dict = collections.defaultdict(dict)
    for course in courses:
        if course['name'] in cleansed_courses_dict:
            cleansed_courses_dict[course['name']]['category'] += course['category']
        else:
            cleansed_courses_dict[course['name']] = course
    cleansed_courses = []
    for course_name, course_info in cleansed_courses_dict.items():
        cleansed_courses.append(course_info)
    return cleansed_courses
