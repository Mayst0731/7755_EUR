import copy
import re

from format_output import location_map, language_map, map_word
from write_to_json import read_from_json, write_to_json


def online_live_desc_2():
    details = read_from_json('final_files/en_compre_detail_7755_EUR_XW_1117.json')
    for detail in details:
        location = detail.get('location')
        total_duration_desc = detail.get('duration_desc')+detail.get('second_duration_desc')+detail.get(
            'third_duration_desc')
        if 'meeting' in total_duration_desc:
            detail['type'] = 'blended-ov'
            continue
        if "," in location and 'Online' in location:
            detail['type'] = 'blended-os'
            continue
        duration_desc = detail.get('duration_desc')
        if 'live' in duration_desc and 'online' in duration_desc:
            detail['type'] = 'blended-ov'
            continue
        elif 'live' in duration_desc:
            detail['type'] = 'blended-ov'
            continue
        else:
            detail['type'] = 'onsite'
    write_to_json(details, './final_files/type_en_compre_detail.json')


def add_modified_loc_3():
    details = read_from_json('./final_files/type_en_compre_detail.json')
    for detail in details:
        locs = detail.get('location')
        detail["location"] = location_map(locs)
        lang = detail.get('languages')
        detail["languages"] = language_map(lang)
    write_to_json(details, './final_files/loc_type_en_compre_detail_4.json')


def duration_desc_integrate():
    details = read_from_json('./final_files/loc_type_en_compre_detail_4.json')
    for detail in details:
        duration_desc = detail.get('duration_desc')+" "+detail.get('second_duration_desc')+" "+detail.get(
            'third_duration_desc')+" " + detail.get('consecutive_desc')
        detail["duration_desc"] = map_word(duration_desc)
        detail["duration_desc"] = detail["duration_desc"].strip()
        detail["duration_desc"] = detail["duration_desc"].replace('  ',', ')
        del detail['second_duration_desc']
        del detail['third_duration_desc']
        detail['effective_date_start'] = detail['effective_start_date']
        del detail['effective_start_date']
        del detail['consecutive_desc']
    write_to_json(details, './final_files/duration_loc_type_en_compre_detail_5.json')


def duration_num(duration_desc, url):
    if url == 'https://www.nyenrode.nl/opleidingen/p/behavioral-and-cultural-governance':
        return 10
    if "3 x 2" in duration_desc:
        return 6
    if 'weekly' in duration_desc and 'meetings' in duration_desc:
        number = re.findall(r'(\d+\s(meetings))', duration_desc)[0][0]
        number = re.findall(r'\d+',number)[0]
        return number
    elif 'weeks' in duration_desc and 'meetings' in duration_desc:
        number = re.findall(r'(\d+\s(weeks))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number
    elif 'meetings' in duration_desc:
        try:
            number = re.findall(r'(\d+\s(meetings))', duration_desc)[0][0]
            number = re.findall(r'\d+', number)[0]
            return number
        except:
            print(f'invalid duration: {duration_desc}  {url}')
    if 'lecture' in duration_desc and 'Monday' in duration_desc:
        number = re.findall(r'(\d+\s(lecture))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number
    if 'modules' in duration_desc and 'week' in duration_desc:
        number = re.findall(r'(\d+\s(modules))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number
    if 'block' in duration_desc:
        return 6
    if 'weekly' in duration_desc and 'days' in duration_desc:
        number = re.findall(r'(\d+\s(days))', duration_desc)[0][0]
        number = re.findall(r'\d+',number)[0]
        return number
    if 'scattered' in duration_desc and 'days' in duration_desc:
        number = re.findall(r'(\d+\s(days))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number
    if 'year' in duration_desc:
        number = re.findall(r'(\d+\s(year))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number
    if 'month' in duration_desc:
        number = re.findall(r'(\d+\s(month))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number
    if "weekly" not in duration_desc and 'week' in duration_desc:
        try:
            number = re.findall(r'(\d+\s(week))', duration_desc)[0][0]
            number = re.findall(r'\d+', number)[0]
            return number
        except:
            print(f'week invalid $$$$$ {duration_desc}, {url}')
    if 'collegedays' in duration_desc:
        number = re.findall(r'(\d+\s(collegedays))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number
    if 'day' in duration_desc:
        try:
            number = re.findall(r'(\d+\s(day))', duration_desc)[0][0]
            number = re.findall(r'\d+', number)[0]
            return number
        except:
            print(f'day invalid $$$$$ {duration_desc}, {url}')
    if 'lecture' in duration_desc:
        try:
            number = re.findall(r'(\d+\s(lecture))', duration_desc)[0][0]
            number = re.findall(r'\d+', number)[0]
        except:
            number = 0
        return number
    if 'hour' in duration_desc:
        number = re.findall(r'(\d+\s(hour))', duration_desc)[0][0]
        number = re.findall(r'\d+', number)[0]
        return number


def duration_type(duration_desc):
    if "3 x 2" in duration_desc:
        return 'days'
    if 'weeks' in duration_desc and 'meetings' in duration_desc:
        return 'weeks'
    if 'meetings' in duration_desc:
        return 'days'
    if 'lecture' in duration_desc and 'Monday' in duration_desc:
        return 'days'
    if 'modules' in duration_desc and 'week' in duration_desc:
        return 'weeks'
    if 'weekly' in duration_desc:
        return 'days'
    if 'block' in duration_desc:
        return 'weeks'
    if 'scattered' in duration_desc and 'days' in duration_desc:
        return 'days'
    if 'year' in duration_desc:
        return 'years'
    if 'month' in duration_desc:
        return 'months'
    if 'week' in duration_desc:
        return 'weeks'
    if 'collegedays' in duration_desc:
        return 'days'
    if 'day' in duration_desc:
        return 'days'
    if 'lecture' in duration_desc:
        return 'days'
    if 'hour' in duration_desc:
        return 'hours'


def print_out_all_durations():
    details = read_from_json('./final_files/duration_loc_type_en_compre_detail_5.json')
    for detail in details:
        print(detail['duration_desc'])


def re_write_duration_info():
    details = read_from_json('./final_files/duration_loc_type_en_compre_detail_5.json')
    for detail in details:
        if detail['url'] == "https://www.nyenrode.nl/opleidingen/p/module-de-verzekeringssector-in-turbulente-tijden-pe-programma-deskundigheidsbevordering":
            detail["effective_date_start"] = '2022-01-01'
        if detail["effective_date_start"] == '2022--':
            detail["effective_date_start"] = '2022-02-01'
        if detail["effective_date_start"] == '2021--':
            detail["effective_date_start"] = '2021-11-01'
        if detail["effective_date_start"] == "2020--":
            detail["effective_date_start"] = '2021-11-01'
        if 'Online' in detail['name']:
            detail['type'] = 'online - self-paced'
        duration_desc = detail.get('duration_desc')
        type = duration_type(duration_desc)
        if not type:
            dur_num = ''
            print(f'invalid duration: {duration_desc}, {detail["url"]}')
        else:
            dur_type = 'duration_' + type
            dur_num = duration_num(duration_desc, detail['url'])
            detail[dur_type] = dur_num
        detail["schedule"] = [
            detail.get('effective_date_start', ''),
            '',
            str(dur_num),
            'formal'
        ]
        if type == 'years':
            print(detail['url'], 'takes multiple years')
        del detail["duration_desc"]
        if not detail["location"]:
            detail['location'] = ["Breukelen, ----, Netherlands"]
        elif detail["location"][0] == "Multiple locations":
            detail['location'] = ["Breukelen, ----, Netherlands"]
        location_set = set(detail.get('location'))
        detail['location'] = list(location_set)
        detail['active'] = True
        detail['priority'] = 0
        detail['publish'] = 100
        detail['is_advanced_management_program'] = True
        tuition = detail.get('tuition', 0)
        if tuition == '':
            tuition = 0
        detail['tuition_number'] = int(tuition)
        del detail['tuition']
        detail['Repeatable'] = 'Y'
        detail['credential'] = get_credetail(detail)
        detail['course_takeaways'] = ''
        detail['who_attend_desc'] = ''
        detail['overview'] = {}
        detail['schedule'] = [detail['schedule']]
        detail['version'] = 1
    write_to_json(details, 'final_files/detail_7755_EUR_XW_1117.json')


def get_credetail(detail):
    if "MBAs" in detail["category"]:
        return 'MBA'
    elif "Masters" in detail["category"]:
        return 'Masters'
    elif "Bachelors" in detail["category"]:
        return 'Bachelor'
    elif 'certifi' in detail['url']:
        return 'Certificate'
    return ''


def test_tuition():
    details = read_from_json('final_files/detail_7755_EUR_XW_1117.json')
    for detail in details:
        tuition = detail['tuition']
        if not isinstance(tuition, int):
            print(tuition)
        if tuition < 10:
            print(tuition)
        if 'tuition_number' in detail:
            print('no')


def test_duplicate():
    du_set = set()
    details = read_from_json('final_files/detail_7755_EUR_XW_1117.json')
    for detail in details:
        if detail['name'] not in du_set:
            du_set.add(detail['name'])
        else:
            print(detail['name'])


def add_three_new_courses():
    details = read_from_json('final_files/detail_7755_EUR_XW_1117.json')
    last_course = details[-1]
    course_1 = change_course_attrs('Bedrijfsleven',
                                    'Maatwerk / InCompany',
               'https://www.nyenrode.nl/opleidingen/executive-education/maatwerk-incompany/bedrijfsleven',
                                   last_course)
    course_2 = change_course_attrs('Overheid en zorg',
                                   'Maatwerk / InCompany',
                                   'https://www.nyenrode.nl/opleidingen/executive-education/maatwerk-incompany/overheid-en-zorg',
                                   last_course)
    course_3 = change_course_attrs('Financiële en zakelijke dienstverlening',
                                   'Maatwerk / InCompany',
                                   'https://www.nyenrode.nl/opleidingen/executive-education/maatwerk-incompany/financi%C3%ABle-en-zakelijke-dienstverlening',
                                   last_course)
    details.append(course_1)
    details.append(course_2)
    details.append(course_3)
    write_to_json(details, 'final_files/detail_7755_EUR_XW_1117.json')


def change_course_attrs(name,
                        category,
                        url,
                        last_course):
    course = copy.deepcopy(last_course)
    course['name'] = name
    course['category'] = [category]
    course['url'] = url
    course['tuition_number'] = 0
    course['effective_date_start'] = ''
    course['schedule'] = [['', '', '', 'formal']]
    course['tuition_note'] = ''
    course["credential"] = ''
    course['duration_years'] = '0'
    return course



online_live_desc_2()
add_modified_loc_3()
duration_desc_integrate()
print_out_all_durations()
re_write_duration_info()
add_three_new_courses()