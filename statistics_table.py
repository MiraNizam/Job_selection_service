from terminaltables import AsciiTable
from hh_statistics import main as hh_main
from sj_statistics import main as sj_main


def create_table(statistics: dict, title: str):
    TABLE_DATA = []
    headers = ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    TABLE_DATA.append(headers)
    for language, statistics_data in statistics.items():
        TABLE_DATA.append([language,
                           statistics_data['vacancies_found'],
                           statistics_data['vacancies_processed'],
                           statistics_data['average_salary']
                           ])
    table = AsciiTable(TABLE_DATA, title)
    print(table.table)


def main():
    hh_title = "HeadHunter Moscow"
    sj_title = "SuperJob Moscow"
    hh_statistics = hh_main()
    sj_statistics = sj_main()
    create_table(hh_statistics, hh_title)
    create_table(sj_statistics, sj_title)


if __name__ == '__main__':
    main()
