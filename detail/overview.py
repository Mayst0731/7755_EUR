def parse_detail_for_one_course(page, course, no_info_course):
    print(f'{course["name"]} is processing**: {course["url"]}')
    map = {"Locatie": "location",
           "Location": "location",
           "Startdatum": "effective_start_date",
           "Start date": "effective_start_date",
           "Duur": "duration_desc",
           "Wekelijkse studie": "duration_desc",
           "Expensive": "duration_desc",
           "Colleges": "consecutive_desc",
           "Languages": "languages",
           "Languages ": "languages",
           "Talen": "languages",
           "Fee": "price",
           "Fee ": "price",
           "Fairy ": "price",
           "Weekly study": "second_duration_desc",
           "Accreditations ": "third_duration_desc",
           "Investering": "price"}

    info = {"location": "",
            "effective_start_date": "",
            "duration_desc": "",
            "consecutive_desc": "",
            "languages": "",
            "price": "",
            "second_duration_desc": "",
            "third_duration_desc": ""}

    info_div = page.find('div', attrs={"class": "program-general-info"})
    info_sessions = None
    if info_div:
        info_sessions = info_div.find_all('div', attrs={"class": "info-item"})

    if not info_sessions:
        print(f'-------{course["url"]} not div')
        no_info_course.append(course)
    elif info_sessions:
        for info_session in info_sessions:
            try:
                label = info_session.find('label')
                label_text = label.text.strip()
                info_attr = map.get(label_text, '')
                if "Wekeli" in label_text:
                    info_attr = "duration_desc"
                elif "Permanente educatie" in label_text:
                    continue
                elif "Accreditaties" in label_text:
                    continue
                elif "Deadline voor aanmelding" in label_text:
                    continue
                res = info_session.find('div')
                res_text = res.text.strip()
                info[info_attr] = res_text
            except Exception as e:
                print(f'{course["url"]} has problem of {e}')
                continue
        # print(title)
    detail = {**course, **info}
    # pprint(detail)
    return detail


# page = requests.get("https://www.nyenrode.nl/opleidingen/p/collegereeks-excellent-leiderschap")
# page = requests.get("https://www.nyenrode.nl/opleidingen/p/behavioral-and-cultural-governance")
# page = requests.get("https://www.nyenrode.nl/opleidingen/p/advanced-management-program")
# page = requests.get("https://www.nyenrode.nl/opleidingen/p/mba-thesis")
# course = {"name": "",
#           "url": ""}
# page = page.text
# page = bs4.BeautifulSoup(page, 'html.parser')
#
# detail = get_detail_for_one_course(page, course, [])
# pprint(detail)
