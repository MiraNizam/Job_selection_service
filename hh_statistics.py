from itertools import count

import requests
from environs import Env

from predict_salary import predict_salary


def get_hh_vacancies(url: str, language: str) -> list:
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
        response = requests.get(f"{url}/vacancies", params=payload)
        response.raise_for_status()
        vacancies = response.json()
        total_vacancies.append(vacancies)
        if page > int(vacancies["found"] / per_page) or page >= (max_count_results / per_page) - 1:
            break
    return total_vacancies


def get_hh_statistics(total_vacancies: list) -> dict:
    sum_salaries = 0
    vacancies_processed = 0
    vacancies_found = 0
    average_salary = 0
    for page_vacancies in total_vacancies:
        vacancies_found = page_vacancies["found"]
        for vacancy in page_vacancies["items"]:
            expected_salary = predict_salary(vacancy["salary"], "from", "to", "RUR")
            if not expected_salary:
                continue
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


def main():
    env = Env()
    env.read_env()

    LANGUAGES = env.list("LANGUAGES")
    URL = "https://api.hh.ru"

    general_statistics = {}
    for language in LANGUAGES:
        total_vacancies = get_hh_vacancies(URL, language)
        language_statistics = get_hh_statistics(total_vacancies)
        general_statistics[language] = language_statistics
    return general_statistics
