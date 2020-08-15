import hh
import sj
from terminaltables import AsciiTable
from dotenv import load_dotenv


def print_table(lst, title):
    table_data = []
    titles = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_data.append(titles)
    for stats in lst:
        for lang in stats:
            values = [lang, stats[lang]['vacancies_found'], stats[lang]['vacancies_processed'],
                      stats[lang]['average_salary']]
            table_data.append(values)
    table = AsciiTable(table_data, title)
    return print(table.table)


if __name__ == "__main__":
    load_dotenv()
    print_table(sj.stats_list_sj, 'SuperJob Moscow')
    print_table(hh.stats_list_hh, 'HeadHunter Moscow')
