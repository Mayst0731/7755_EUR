import re
from pprint import pprint
from write_to_json import read_from_json, write_to_json


def format_date(ori_start_date):
    if ori_start_date == "2021/2022":
        return "2022-01-01"
    date = ''
    day = ''
    month = ''
    year = ''
    if not hasNumbers(ori_start_date):
        return ''
    try:
        day = find_date(ori_start_date)
        if len(day) == 1:
            day = '0'+day
        month = map_month(ori_start_date)
        year = find_year(ori_start_date)
        date = f'{year}-{month}-{day}'
    except:
        print(ori_start_date, ' not valid')
    if not year and not month:
        return ''
    elif year and month and not day:
        return f'{year}-{month}-01'
    return date


def get_currency(price):
    if "€" in price:
        return 'EUR'
    return 'EUR'


def get_tuition(price):
    price_list = price.split(' ')
    tuition = ''
    for s in price_list:
        if hasNumbers(s):
            tuition = ''.join(re.findall('\d+', s))
            break
    return tuition


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def find_year(ori_start_date):
    has_year = re.search(r'\d{4}', ori_start_date)
    if not has_year:
        return ''
    year = re.findall(r'\d{4}', ori_start_date)[0]
    return year


def find_date(ori_start_date):
    day = re.findall(r'\b\d{1,2}\b', ori_start_date)
    if day:
        day = day[0]
    else:
        day = ''
    return day


def map_month(ori_start_date):
    mapping = {"januari": "01",
               "februari": "02",
               "maart": "03",
               "april": "04",
               "mei": "05",
               "juni": "06",
               "juli": "07",
               "augustus": "08",
               "september": "09",
               "oktober": "10",
               "november": "11",
               "december": "12"}
    for mon_str, month in mapping.items():
        if mon_str in ori_start_date:
            return month
    return ''


def integrate_duration_desc(detail):
    duration = []
    first_duration = detail.get('duration_desc')
    second_duration = detail.get('second_duration_desc')
    third_duration = detail.get('third_duration_desc')
    duration = [first_duration, second_duration, third_duration]
    pprint(duration)
    return duration


# for date in start_dates:
#     final_date = format_date(date)
#     print(f'{date}  -->   {final_date}')

# for price in prices:
#     final_price = get_tuition(price)
#     print(f'{price} ---->  {final_price}')
def collect_word_set(details):
    word_set = set()
    for detail in details:
        duration_words = ''
        duration_words += detail.get('duration_desc')
        duration_words += detail.get('second_duration_desc')
        duration_words += detail.get('third_duration_desc')
        duration_words_lst = duration_words.split()
        for word in duration_words_lst:
            if len(word)>1 and not word.isdigit():
                word_set.add(word)
    return word_set


def map_word(duration_desc):
    mapping = {"huiswerk": "homework",
               "bijeenkomsten": "meetings",
               'terugkomdays':"return days",
               "maximaal": "maximum",
               "afstudeerscriptie": "graduation thesis",
               "wekelijks": "weekly",
               "voorbereiding":"preparation",
               "dagen": "days",
               "reünie": "reunion",
               "verspreid": "scattered",
               "weken": "weeks",
               "maanday": "Monday",
               "scriptie": "thesis",
               "uitgesteld": "postponed",
               "Aanmelddeadline": "Registration deadline",
               "PE-punten": "PE-points",
               "terugkomdagen": "return days",
               "bijeenkomst": "meeting",
               "blokken" : "block",
               "colleges": "lecture",
               "dag": "day",
               "dagdeel": "daypart",
               "dagenmaximaal": "part-time",
               "deeltijd": "diploma",
               "inclusief": "including",
               "jaar": "year",
               "leertraject": "learning-path",
               "keer":"times",
               "Vrijday": "Friday",
               "maanden": "months",
               "Donderdaymidday": "Thursday afternoon",
               "avond": "evening",
               "meer": "module",
               "optionele": "optional",
               "overnachting": "overnight",
               "uur": "hour",
               "week": "week",
               "zelfstudie": "self-study",
               "van": "from",
               "en": "and",
               "tot": "until",
               "op": 'on',
               "Van": "from"}

    for du_key, en_val in mapping.items():
        if du_key in duration_desc:
            duration_desc = duration_desc.replace(du_key, en_val)
    return duration_desc


def language_map(ori_lang):
    lang_map = {"Engels": "English",
                "Nederlands": "Dutch"}
    return lang_map.get(ori_lang, "Dutch")


def location_map(locs):
    if locs == "Online":
        return ["Amsterdam, ----, Netherlands"]
    formatted_locations = []
    location_map = {"Amsterdam": "Amsterdam, ----, Netherlands",
                    "Breukelen": "Breukelen, ----, Netherlands",
                    "Den Haag": "Den Haag, ----, Netherlands",
                    "Delft": "Delft, ----, Netherlands",
                    "Noordwijk":"Noordwijk, ----, Netherlands",
                    }
    if "Meerdere locaties" in locs:
        return ["Multiple locations"]
    if ',' in locs:
        locs = locs.replace(',', '')
    locs_lst = locs.split()
    for key, val in location_map.items():
        for loc in locs_lst:
            loc = loc.strip()
            if loc in key:
                new_loc = val
                formatted_locations.append(new_loc)
    return formatted_locations


def modify_to_en_duration_and_rewrite_1():
    details = read_from_json('final_files/comprehensive_detail_7755_EUR_XW_1117.json')
    for detail in details:
        ori_duration_desc = detail.get('duration_desc')
        en_duration_desc = map_word(ori_duration_desc)
        detail["duration_desc"] = en_duration_desc
        ori_duration_desc = detail.get('second_duration_desc')
        sec_en_duration_desc = map_word(ori_duration_desc)
        detail["second_duration_desc"] = sec_en_duration_desc
        ori_duration_desc = detail.get('third_duration_desc')
        third_en_duration_desc = map_word(ori_duration_desc)
        detail["third_duration_desc"] = third_en_duration_desc

        ori_consecutive = detail.get('consecutive_desc')
        en_consecutive = map_word(ori_consecutive)
        detail["consecutive_desc"] = en_consecutive

        ori_date = detail.get("effective_start_date")
        detail["effective_start_date"] = format_date(ori_date)

        price = detail.get('price')
        detail["currency"] = get_currency(price)
        detail["tuition"] = get_tuition(price)
        detail["tuition_note"] = price
        del detail["price"]
    write_to_json(details, 'final_files/en_compre_detail_7755_EUR_XW_1117.json')


def print_no_name_att():
    details = read_from_json('final_files/detail_7755_EUR_XW_1117.json')
    for detail in details:
        if "" in detail:
            print(detail["url"], detail[""])


# print_no_name_att()


modify_to_en_duration_and_rewrite_1()
