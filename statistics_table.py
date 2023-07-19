from terminaltables import AsciiTable

from hh_statistics import main as get_hh_statistics
from sj_statistics import main as get_sj_statistics


def create_table(statistics: dict, title: str):
    table_fields = []
    headers = ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    table_fields.append(headers)
    for language, statistics_data in statistics.items():
        table_fields.append([language,
                           statistics_data['vacancies_found'],
                           statistics_data['vacancies_processed'],
                           statistics_data['average_salary']
                           ])
    table = AsciiTable(table_fields, title)
    return table.table


def main():
    hh_title = "HeadHunter Moscow"
    sj_title = "SuperJob Moscow"
    hh_statistics = get_hh_statistics()
    sj_statistics = get_sj_statistics()
    print(create_table(hh_statistics, hh_title))
    print(create_table(sj_statistics, sj_title))


if __name__ == '__main__':
    main()
