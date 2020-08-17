import requests
import numpy
from itertools import count

HH_URL_TEMPLATE = 'https://api.hh.ru/{}/'
MAXIMAL_PAGE = 98


def get_vacancies(profession):
    all_pages = []
    for page in count(0):
        params = {'text': profession, 'period': 30, 'area': '1', 'page': page}
        response = requests.get(HH_URL_TEMPLATE.format('vacancies'), params=params)
        response.raise_for_status()
        hh_response = response.json()
        all_pages.append(hh_response)
        if page == hh_response['pages'] or page > MAXIMAL_PAGE:
            break
    return all_pages


def get_salaries_average(salary_from, salary_to):
    if salary_from == 0 or salary_from is None:
        return salary_to * 1.2
    if salary_to == 0 or salary_to is None:
        return salary_from * 0.8
    if salary_from is not None and salary_to is not None:
        return (salary_from + salary_to) / 2


def predict_rub_salary(vacancy):
    salary = []
    for all_pages in get_vacancies(vacancy):
        for items in all_pages['items']:
            if items['salary'] is None:
                continue
            if items['salary']['currency'] != 'RUR':
                continue
            if get_salaries_average(items['salary']['from'], items['salary']['to']) is None:
                continue
            else:
                salary.append(get_salaries_average(items['salary']['to'], items['salary']['from']))
    return salary


def get_stats():
    languages_list = ['Go', 'C', 'C#', 'CSS', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    stats = []
    for language in languages_list:
        language_vacancies_amount_hh = {
            language: {'vacancies_found': get_vacancies('{} программист'.format(language))[0]['found'],
                       'vacancies_processed': len(get_vacancies('{} программист'.format(language))),
                       'average_salary': int(
                           numpy.mean(predict_rub_salary('{} программист'.format(language))[0])),
                       }
        }
        stats.append(language_vacancies_amount_hh)
    return stats
