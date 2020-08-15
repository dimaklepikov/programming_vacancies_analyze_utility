import numpy
import requests
import os


SUPERJOB_URL_TEMPLATE = 'https://api.superjob.ru/2.0/{}'
API_KEY_SJ = os.getenv('sj_secret_key')


def get_superjob_vacancies(vacancy, page=0):
    all_pages = []
    headers = {'X-Api-App-Id': API_KEY_SJ}
    params = {'keyword': vacancy, 'town': 4, 'catalogues': 48, 'page': page}
    response = requests.get(SUPERJOB_URL_TEMPLATE.format('vacancies'), headers=headers, params=params)
    response.raise_for_status()
    all_pages.append(response.json())
    while response.json()['more'] is True:
        params = {'keyword': vacancy, 'town': 4, 'catalogues': 48, 'page': page}
        response = requests.get(SUPERJOB_URL_TEMPLATE.format('vacancies'), headers=headers, params=params)
        response.raise_for_status()
        all_pages.append(response.json())
        page += 1
    return all_pages


def predict_rub_salary_for_SuperJob(vacancy):
    salaries_average = []
    for all_vac in get_superjob_vacancies(vacancy):
        for objects in all_vac['objects']:
            if objects['payment_from'] == 0 and objects['payment_to'] == 0:
                continue
            if objects['payment_from'] == 0:
                salaries_average.append(objects['payment_to'] * 1.2)
            if objects['payment_to'] == 0:
                salaries_average.append(objects['payment_from'] * 0.8)
            if objects['payment_from'] and objects['payment_to'] is int:
                salaries_average.append((objects['payment_from'] + objects['payment_to']) / 2)
    return salaries_average


languages_list = ['Go', 'C', 'C#', 'CSS', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
stats_list_sj = []
for language in languages_list:
    language_vacancies_amount_sj = {
        language: {'vacancies_found': get_superjob_vacancies('{} программист'.format(language))[0]['total'],
                   'vacancies_processed': len(predict_rub_salary_for_SuperJob('{} программист'.format(language))),
                   'average_salary': int(
                       numpy.mean(predict_rub_salary_for_SuperJob('{} программист'.format(language)))),
                   }
    }
    stats_list_sj.append(language_vacancies_amount_sj)
