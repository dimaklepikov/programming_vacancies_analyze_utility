import hh
import sj
from terminaltables import AsciiTable
from dotenv import load_dotenv


def print_table(body, title):
    table_content = []
    titles = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_content.append(titles)
    for stats in body:
        for lang in stats:
            values = [lang, stats[lang]['vacancies_found'], stats[lang]['vacancies_processed'],
                      stats[lang]['average_salary']]
            table_content.append(values)
    table = AsciiTable(table_content, title)
    return print(table.table)


if __name__ == "__main__":
    load_dotenv()
    print_table(sj.get_stats(), 'SuperJob Moscow')
    print_table(hh.get_stats(), 'HeadHunter Moscow')
