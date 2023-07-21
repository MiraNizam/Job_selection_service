from itertools import count

import requests

from predict_salary import predict_salary


def get_hh_vacancies(language: str) -> list:
    hh_api_url = "https://api.hh.ru"
    total_vacancies = []
    for page in count():
        period_days = 30
        per_page = 100
        max_count_results = 2000
        payload = {
            "text": f"программист {language}",
            "area": "1",  # Москва
            "period": period_days,
            "currency": "RUR",
            "per_page": per_page,
            "page": page
        }
        response = requests.get(f"{hh_api_url}/vacancies", params=payload)
        response.raise_for_status()
        vacancies = response.json()
        total_vacancies.append(vacancies)
        if page > int(vacancies["found"] / per_page) or page >= (max_count_results / per_page) - 1:
            break
    return total_vacancies


def get_hh_page_statistics(total_vacancies: list) -> dict:
    sum_salaries = 0
    vacancies_processed = 0
    vacancies_found = 0
    for page_vacancies in total_vacancies:
        vacancies_found = page_vacancies["found"]
        for vacancy in page_vacancies["items"]:
            if not vacancy["salary"] or vacancy["salary"]["currency"] != "RUR":
                continue
            from_salary = vacancy["salary"]["from"]
            to_salary = vacancy["salary"]["to"]
            expected_salary = predict_salary(from_salary, to_salary)
            sum_salaries += expected_salary
            vacancies_processed += 1
    try:
        average_salary = int(sum_salaries / vacancies_processed)
    except ZeroDivisionError:
        average_salary = 0

    language_statistics = {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return language_statistics


def get_hh_statistics(languages: list):
    general_statistics = {}
    for language in languages:
        total_vacancies = get_hh_vacancies(language)
        language_statistics = get_hh_page_statistics(total_vacancies)
        general_statistics[language] = language_statistics
    return general_statistics
