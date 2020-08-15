import requests
import numpy
from itertools import count

HH_URL_TEMPLATE = 'https://api.hh.ru/{}/'


def get_vacancies(profession, page=0):
    all_pages = []
    for page in count(0):
        params = {'text': profession, 'period': 30, 'area': '1', 'page': page}
        response = requests.get(HH_URL_TEMPLATE.format('vacancies'), params=params)
        response.raise_for_status()
        all_pages.append(response.json())
        page += 1
        if page > response.json()['pages']:
            break
    return all_pages


print(get_vacancies('python'))


def predict_rub_salary(vacancy):
    salaries_average = []
    for all_pages in get_vacancies(profession=vacancy):
        for items in all_pages['items']:
            if items['salary'] is None:
                continue
            if items['salary']['currency'] != 'RUR':
                continue
            if items['salary']['to'] is None:
                salaries_average.append(items['salary']['from'] * 1.2)
            if items['salary']['from'] is None:
                salaries_average.append(items['salary']['to'] * 0.8)
            if items['salary']['to'] and items['salary']['from'] is int:
                salaries_average.append((items['salary']['from'] + items['salary']['to']) / 2)
    return salaries_average


languages_list = ['Go', 'C', 'C#', 'CSS', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
stats_list_hh = []
for language in languages_list:
    language_vacancies_amount_hh = {
        language: {'vacancies_found': get_vacancies('{} программист'.format(language))[0]['found'],
                   'vacancies_processed': len(get_vacancies('{} программист'.format(language))),
                   'average_salary': int(
                       numpy.mean(get_vacancies('{} программист'.format(language)))),
                   }
    }
    stats_list_hh.append(language_vacancies_amount_hh)


