import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from hh_statistics import get_hh_statistics
from sj_statistics import get_sj_statistics


def create_table(statistics: dict, title: str):
    table_fields = []
    headers = ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    table_fields.append(headers)
    for language, language_statistics in statistics.items():
        table_fields.append([language,
                           language_statistics['vacancies_found'],
                           language_statistics['vacancies_processed'],
                           language_statistics['average_salary']
                           ])
    table = AsciiTable(table_fields, title)
    return table.table


def main():
    load_dotenv()
    secret_key = os.getenv("SJ_SECRET_KEY")
    languages = ["JavaScript","Java","Python","PHP","C++","C#","C"]
    hh_title = "HeadHunter Moscow"
    sj_title = "SuperJob Moscow"
    hh_statistics = get_hh_statistics(languages)
    sj_statistics = get_sj_statistics(secret_key, languages)
    print(create_table(hh_statistics, hh_title))
    print(create_table(sj_statistics, sj_title))


if __name__ == '__main__':
    main()
