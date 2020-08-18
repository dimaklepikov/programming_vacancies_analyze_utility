import requests
import numpy
from itertools import count
from utils import get_salaries_average

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
                       'vacancies_processed': len(predict_rub_salary('{} программист'.format(language))),
                       'average_salary': int(
                           numpy.mean(predict_rub_salary('{} программист'.format(language))[0])),
                       }
        }
        stats.append(language_vacancies_amount_hh)
    return stats
