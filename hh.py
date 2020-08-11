import requests
import numpy
from terminaltables import AsciiTable

HH_URL_TEMPLATE = 'https://api.hh.ru/'


def get_vacancies(profession, page=0):
    all_pages = []
    params = {'text': profession, 'period': 30, 'area': '1', 'page': page}
    response = requests.get('{}vacancies/'.format(HH_URL_TEMPLATE), params=params)
    response.raise_for_status()
    while page < response.json()['pages']:
        params = {'text': profession, 'period': 30, 'area': '1', 'page': page}
        response = requests.get('{}vacancies/'.format(HH_URL_TEMPLATE), params=params)
        response.raise_for_status()
        all_pages.append(response.json())
        page += 1
    return all_pages


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


language_vacancies_amount_hh = {
    'Go': {'vacancies_found': get_vacancies('Go программист')[0]['found'],
           'vacancies_processed': len(predict_rub_salary('Python программист')),
           'average_salary': int(numpy.mean(predict_rub_salary('Python программист'))),
           },
    'C': {'vacancies_found': get_vacancies('C программист')[0]['found'],
          'vacancies_processed': len(predict_rub_salary('C программист')),
          'average_salary': int(numpy.mean(predict_rub_salary('C программист'))),
          },
    'C#': {'vacancies_found': get_vacancies('C# программист')[0]['found'],
           'vacancies_processed': len(predict_rub_salary('C# программист')),
           'average_salary': int(numpy.mean(predict_rub_salary('C# программист'))),
           },
    'CSS': {'vacancies_found': get_vacancies('Go программист')[0]['found'],
            'vacancies_processed': len(predict_rub_salary('Python программист')),
            'average_salary': int(numpy.mean(predict_rub_salary('Python программист'))),
            },
    'C++': {'vacancies_found': get_vacancies('C++ программист')[0]['found'],
            'vacancies_processed': len(predict_rub_salary('C++ программист')),
            'average_salary': int(numpy.mean(predict_rub_salary('C++ программист'))),
            },
    'PHP': {'vacancies_found': get_vacancies('PHP программист')[0]['found'],
            'vacancies_processed': len(predict_rub_salary('PHP программист')),
            'average_salary': int(numpy.mean(predict_rub_salary('PHP программист'))),
            },
    'Ruby': {'vacancies_found': get_vacancies('Ruby программист')[0]['found'],
             'vacancies_processed': len(predict_rub_salary('Ruby программист')),
             'average_salary': int(numpy.mean(predict_rub_salary('Ruby программист'))),
             },
    'Python': {'vacancies_found': get_vacancies('Python программист')[0]['found'],
               'vacancies_processed': len(predict_rub_salary('Python программист')),
               'average_salary': int(numpy.mean(predict_rub_salary('Python программист'))),
               },
    'Java': {'vacancies_found': get_vacancies('Java программист')[0]['found'],
             'vacancies_processed': len(predict_rub_salary('Java программист')),
             'average_salary': int(numpy.mean(predict_rub_salary('Java программист'))),
             },
    'JavaScript': {'vacancies_found': get_vacancies('JavaScript программист')[0]['found'],
                   'vacancies_processed': len(predict_rub_salary('JavaScript программист')),
                   'average_salary': int(numpy.mean(predict_rub_salary('JavaScript программист'))),
                   },
}


def print_table(stats_dict):
    title = 'HeadHunter Moscow'
    stats_dict = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
        ['Go', language_vacancies_amount_hh['Go']['vacancies_found'],
         language_vacancies_amount_hh['Go']['vacancies_processed'],
         language_vacancies_amount_hh['Go']['average_salary']],
        ['C', language_vacancies_amount_hh['C']['vacancies_found'],
         language_vacancies_amount_hh['C']['vacancies_processed'],
         language_vacancies_amount_hh['C']['average_salary']],
        ['C#', language_vacancies_amount_hh['C#']['vacancies_found'],
         language_vacancies_amount_hh['C#']['vacancies_processed'],
         language_vacancies_amount_hh['C#']['average_salary']],
        ['CSS', language_vacancies_amount_hh['CSS']['vacancies_found'],
         language_vacancies_amount_hh['CSS']['vacancies_processed'],
         language_vacancies_amount_hh['CSS']['average_salary']],
        ['C++', language_vacancies_amount_hh['C++']['vacancies_found'],
         language_vacancies_amount_hh['C++']['vacancies_processed'],
         language_vacancies_amount_hh['C++']['average_salary']],
        ['PHP', language_vacancies_amount_hh['PHP']['vacancies_found'],
         language_vacancies_amount_hh['PHP']['vacancies_processed'],
         language_vacancies_amount_hh['PHP']['average_salary']],
        ['Ruby', language_vacancies_amount_hh['Ruby']['vacancies_found'],
         language_vacancies_amount_hh['Ruby']['vacancies_processed'],
         language_vacancies_amount_hh['Ruby']['average_salary']],
        ['Python', language_vacancies_amount_hh['Python']['vacancies_found'],
         language_vacancies_amount_hh['Python']['vacancies_processed'],
         language_vacancies_amount_hh['Python']['average_salary']],
        ['Java', language_vacancies_amount_hh['Java']['vacancies_found'],
         language_vacancies_amount_hh['Java']['vacancies_processed'],
         language_vacancies_amount_hh['Java']['average_salary']],
        ['JavaScript', language_vacancies_amount_hh['JavaScript']['vacancies_found'],
         language_vacancies_amount_hh['JavaScript']['vacancies_processed'],
         language_vacancies_amount_hh['JavaScript']['average_salary']],
    ]
    table = AsciiTable(stats_dict, title)
    return print(table.table)
