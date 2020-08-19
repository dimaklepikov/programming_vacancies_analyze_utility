import requests
import os
import numpy
from utils import get_salaries_average

SUPERJOB_URL_TEMPLATE = 'https://api.superjob.ru/2.0/{}/'


def get_sj_vacancy(vacancy, api_key):
    headers = {'X-Api-App-Id': api_key}
    params = {'keyword': vacancy, 'town': 4, 'catalogues': 48}
    response = requests.get(SUPERJOB_URL_TEMPLATE.format('vacancies'), headers=headers, params=params)
    response.raise_for_status()
    sj_response = response.json()
    return sj_response


def get_sj_vacancies(vacancy, api_key, page=0):
    all_pages = []
    sj_response = get_sj_vacancy(vacancy, os.getenv('SJ_SECRET_KEY'))
    if not sj_response['more']:
        all_pages.append(sj_response)
    while sj_response['more']:
        headers = {'X-Api-App-Id': api_key}
        params = {'keyword': vacancy, 'town': 4, 'catalogues': 48, 'page': page}
        response = requests.get(SUPERJOB_URL_TEMPLATE.format('vacancies'), headers=headers, params=params)
        response.raise_for_status()
        sj_response = response.json()
        all_pages.append(sj_response)
        page += 1
    return all_pages


def predict_rub_salary_for_SuperJob(vacancy, api_key):
    salaries = []
    sj_fetched_vacancies = get_sj_vacancies(vacancy, api_key)
    for all_vac in sj_fetched_vacancies:
        for objects in all_vac['objects']:
            payment = get_salaries_average(objects['payment_from'], objects['payment_to'])
            if payment == 0:
                continue
            if payment is None:
                continue
            else:
                salaries.append(payment)
    return salaries


def get_stats():
    programming_languages = ['Go', 'C', 'C#', 'CSS', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    stats = []
    for language in programming_languages:
        language_vacancies_amount_sj = {
            language: {
                'vacancies_found': get_sj_vacancies('{} программист'.format(language),
                                                    os.getenv('SJ_SECRET_KEY'))[0]['total'],
                'vacancies_processed': len(
                    predict_rub_salary_for_SuperJob('{} программист'.format(language), os.getenv('SJ_SECRET_KEY'))),
                'average_salary': int(
                    numpy.mean(predict_rub_salary_for_SuperJob('{} программист'.format(language),
                                                               os.getenv('SJ_SECRET_KEY')))),
            }
        }
        stats.append(language_vacancies_amount_sj)
    return stats
