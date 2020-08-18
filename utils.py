from terminaltables import AsciiTable


def get_salaries_average(salary_from, salary_to):
    if salary_from == 0 or salary_from is None:
        return salary_to * 1.2
    if salary_to == 0 or salary_to is None:
        return salary_from * 0.8
    if salary_from is not None and salary_to is not None:
        return (salary_from + salary_to) / 2


def print_table(table_body_content, title):
    table_content = []
    titles = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_content.append(titles)
    for stats in table_body_content:
        for lang in stats:
            values = [lang, stats[lang]['vacancies_found'], stats[lang]['vacancies_processed'],
                      stats[lang]['average_salary']]
            table_content.append(values)
    table = AsciiTable(table_content, title)
    return print(table.table)
