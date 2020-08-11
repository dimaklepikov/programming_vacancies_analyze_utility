import numpy
import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable

load_dotenv()

SUPERJOB_URL_TEMPLATE = 'https://api.superjob.ru/2.0/'
API_KEY_SJ = os.getenv('sj_secret_key')


def get_superjob_vacancies(vacancy, page=0):
    all_pages = []
    headers = {'X-Api-App-Id': API_KEY_SJ}
    params = {'keyword': vacancy, 'town': 4, 'catalogues': 48, 'page': page}
    response = requests.get('{}vacancies/'.format(SUPERJOB_URL_TEMPLATE), headers=headers, params=params)
    response.raise_for_status()
    all_pages.append(response.json())
    while response.json()['more'] is True:
        params = {'keyword': vacancy, 'town': 4, 'catalogues': 48, 'page': page}
        response = requests.get('{}vacancies/'.format(SUPERJOB_URL_TEMPLATE), headers=headers, params=params)
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


language_vacancies_amount_sj = {
    'Go': {'vacancies_found': get_superjob_vacancies('Go программист')[0]['total'],
           'vacancies_processed': len(predict_rub_salary_for_SuperJob('Go программист')),
           'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('Go программист'))),
           },
    'C': {'vacancies_found': get_superjob_vacancies('C программист')[0]['total'],
          'vacancies_processed': len(predict_rub_salary_for_SuperJob('C программист')),
          'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('C программист'))),
          },
    'C#': {'vacancies_found': get_superjob_vacancies('C# программист')[0]['total'],
           'vacancies_processed': len(predict_rub_salary_for_SuperJob('C# программист')),
           'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('C# программист'))),
           },
    'CSS': {'vacancies_found': get_superjob_vacancies('CSS программист')[0]['total'],
            'vacancies_processed': len(predict_rub_salary_for_SuperJob('CSS программист')),
            'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('CSS программист'))),
            },
    'C++': {'vacancies_found': get_superjob_vacancies('C++ программист')[0]['total'],
            'vacancies_processed': len(predict_rub_salary_for_SuperJob('C++ программист')),
            'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('C++ программист'))),
            },
    'PHP': {'vacancies_found': get_superjob_vacancies('PHP программист')[0]['total'],
            'vacancies_processed': len(predict_rub_salary_for_SuperJob('PHP программист')),
            'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('PHP программист'))),
            },
    'Ruby': {'vacancies_found': get_superjob_vacancies('Ruby программист')[0]['total'],
             'vacancies_processed': len(predict_rub_salary_for_SuperJob('Ruby программист')),
             'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('Ruby программист'))),
             },
    'Python': {'vacancies_found': get_superjob_vacancies('Python программист')[0]['total'],
               'vacancies_processed': len(predict_rub_salary_for_SuperJob('Python программист')),
               'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('Python программист'))),
               },
    'Java': {'vacancies_found': get_superjob_vacancies('Java программист')[0]['total'],
             'vacancies_processed': len(predict_rub_salary_for_SuperJob('Java программист')),
             'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('Java программист'))),
             },
    'JavaScript': {'vacancies_found': get_superjob_vacancies('JavaScript программист')[0]['total'],
                   'vacancies_processed': len(predict_rub_salary_for_SuperJob('JavaScript программист')),
                   'average_salary': int(numpy.mean(predict_rub_salary_for_SuperJob('JavaScript программист'))),
                   },
}


def print_table(stats_dict):
    title = 'SuperJob Moscow'
    stats_dict = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
        ['Go', language_vacancies_amount_sj['Go']['vacancies_found'],
         language_vacancies_amount_sj['Go']['vacancies_processed'],
         language_vacancies_amount_sj['Go']['average_salary']],
        ['C', language_vacancies_amount_sj['C']['vacancies_found'],
         language_vacancies_amount_sj['C']['vacancies_processed'],
         language_vacancies_amount_sj['C']['average_salary']],
        ['C#', language_vacancies_amount_sj['C#']['vacancies_found'],
         language_vacancies_amount_sj['C#']['vacancies_processed'],
         language_vacancies_amount_sj['C#']['average_salary']],
        ['CSS', language_vacancies_amount_sj['CSS']['vacancies_found'],
         language_vacancies_amount_sj['CSS']['vacancies_processed'],
         language_vacancies_amount_sj['CSS']['average_salary']],
        ['C++', language_vacancies_amount_sj['C++']['vacancies_found'],
         language_vacancies_amount_sj['C++']['vacancies_processed'],
         language_vacancies_amount_sj['C++']['average_salary']],
        ['PHP', language_vacancies_amount_sj['PHP']['vacancies_found'],
         language_vacancies_amount_sj['PHP']['vacancies_processed'],
         language_vacancies_amount_sj['PHP']['average_salary']],
        ['Ruby', language_vacancies_amount_sj['Ruby']['vacancies_found'],
         language_vacancies_amount_sj['Ruby']['vacancies_processed'],
         language_vacancies_amount_sj['Ruby']['average_salary']],
        ['Python', language_vacancies_amount_sj['Python']['vacancies_found'],
         language_vacancies_amount_sj['Python']['vacancies_processed'],
         language_vacancies_amount_sj['Python']['average_salary']],
        ['Java', language_vacancies_amount_sj['Java']['vacancies_found'],
         language_vacancies_amount_sj['Java']['vacancies_processed'],
         language_vacancies_amount_sj['Java']['average_salary']],
        ['JavaScript', language_vacancies_amount_sj['JavaScript']['vacancies_found'],
         language_vacancies_amount_sj['JavaScript']['vacancies_processed'],
         language_vacancies_amount_sj['JavaScript']['average_salary']],
    ]
    table = AsciiTable(stats_dict, title)
    return print(table.table)


