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


def predict_rub_salary(hh_fetched_vacancies):
    salaries = []
    for all_pages in hh_fetched_vacancies:
        for items in all_pages['items']:
            if items['salary'] is None:
                continue
            if items['salary']['currency'] != 'RUR':
                continue
            if get_salaries_average(items['salary']['from'], items['salary']['to']) is None:
                continue
            else:
                salaries.append(get_salaries_average(items['salary']['to'], items['salary']['from']))
    return salaries


def get_stats(language):
    all_pages_response = get_vacancies('{} программист'.format(language))
    language_vacancies_amount_hh = {
        language: {'vacancies_found': all_pages_response[0]['found'],
                   'vacancies_processed': len(predict_rub_salary(all_pages_response)),
                   'average_salary': int(
                       numpy.mean(predict_rub_salary(all_pages_response)[0])),
                   }
    }
    return language_vacancies_amount_hh
