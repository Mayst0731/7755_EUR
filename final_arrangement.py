from pprint import pprint
from write_to_json import read_from_json


def check_all_locations(details):
    location_set = set()
    for detail in details:
        location = detail.get('location')
        location_set.add(location)
    return location_set


def check_all_langs(details):
    lan_set = set()
    for detail in details:
        lan = detail.get('languages')
        lan_set.add(lan)
    return lan_set


def check_all_start_date(details):
    start_set = set()
    for detail in details:
        start = detail.get('effective_start_date')
        start_set.add(start)
    return start_set


def check_all_duration(details):
    duration_set = set()
    for detail in details:
        duration = detail.get('duration_desc')
        duration_set.add(duration)
    return duration_set


def check_all_price(details):
    price_set = set()
    for detail in details:
        price = detail.get('price')
        price_set.add(price)
    return price_set


def check_other_missing_info(details):
    other_set = set()
    for detail in details:
        other = detail.get('second_duration_desc','')
        other_set.add(other)
        other = detail.get('third_duration_desc', '')
        other_set.add(other)
    return other_set


def print_out_attr():
    details = read_from_json('final_files/comprehensive_detail_7755_EUR_XW_0527.json')
    print('location')
    location_set = check_all_locations(details)
    pprint(location_set)
    print('*****************************************************************')
    print('langs')
    langs_set = check_all_langs(details)
    pprint(langs_set)
    print('*****************************************************************')
    print('start_date')
    start_set = check_all_start_date(details)
    pprint(start_set)
    print('*****************************************************************')
    print('duration description')
    durations = check_all_duration(details)
    pprint(durations)
    print('*****************************************************************')
    print('price')
    prices = check_all_price(details)
    pprint(prices)
    print('*****************************************************************')
    print('other')
    other_info = check_other_missing_info(details)
    pprint(other_info)



# print_out_attr()


