import requests
import os
import numpy
from hh import get_salaries_average

SUPERJOB_URL_TEMPLATE = 'https://api.superjob.ru/2.0/{}/'


def get_superjob_vacancies(vacancy, page=0):
    all_pages = []
    headers = {'X-Api-App-Id': os.getenv('sj_secret_key')}
    params = {'keyword': vacancy, 'town': 4, 'catalogues': 48, 'page': page}
    response = requests.get(SUPERJOB_URL_TEMPLATE.format('vacancies'), headers=headers, params=params)
    response.raise_for_status()
    sj_response = response.json()
    if sj_response['more'] is False:
        all_pages.append(sj_response)
    while sj_response['more'] is True:
        params = {'keyword': vacancy, 'town': 4, 'catalogues': 48, 'page': page}
        response = requests.get(SUPERJOB_URL_TEMPLATE.format('vacancies'), headers=headers, params=params)
        response.raise_for_status()
        sj_response = response.json()
        all_pages.append(sj_response)
        page += 1
    return all_pages


def predict_rub_salary_for_SuperJob(vacancy):
    salary = []
    for all_vac in get_superjob_vacancies(vacancy):
        for objects in all_vac['objects']:
            if get_salaries_average(objects['payment_from'], objects['payment_to']) == 0:
                continue
            if get_salaries_average(objects['payment_from'], objects['payment_to']) is None:
                continue
            else:
                salary.append(get_salaries_average(objects['payment_from'], objects['payment_to']))
    return salary


def get_stats():
    languages_list = ['Go', 'C', 'C#', 'CSS', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    stats = []
    for language in languages_list:
        language_vacancies_amount_sj = {
            language: {
                'vacancies_found': get_superjob_vacancies('{} программист'.format(language))[0]['total'],
                'vacancies_processed': len(
                    predict_rub_salary_for_SuperJob('{} программист'.format(language))),
                'average_salary': int(
                    numpy.mean(predict_rub_salary_for_SuperJob('{} программист'.format(language)))),
            }
        }
        stats.append(language_vacancies_amount_sj)
    return stats
