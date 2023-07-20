from itertools import count

import requests

from predict_salary import predict_salary


def get_sj_vacancies(secret_key: str, language: str) -> list:
    sj_api_url = "https://api.superjob.ru/2.0"
    per_page = 100
    max_count_results = 500

    headers = {"X-Api-App-Id": secret_key}
    total_vacancies = []
    for page in count():
        payload = {"town": "Москва", "keyword": f"программист {language}", "page": page, "count": per_page}
        response = requests.get(f"{sj_api_url}/vacancies/", headers=headers, params=payload)
        response.raise_for_status()
        vacancies = response.json()
        total_vacancies.append(vacancies)
        if page > vacancies["total"] / per_page or page >= (max_count_results / per_page) - 1:
            break
    return total_vacancies


def get_sj_page_statistics(total_vacancies: list) -> dict:
    sum_salaries = 0
    vacancies_processed = 0
    vacancies_found = 0
    for vacancies in total_vacancies:
        vacancies_found = vacancies["total"]
        for vacancy in vacancies["objects"]:
            from_salary = vacancy["payment_from"]
            to_salary = vacancy["payment_to"]
            if not from_salary and not to_salary or vacancy["currency"] != "rub":
                continue
            else:
                expected_salary = predict_salary(from_salary, to_salary)
                sum_salaries += expected_salary
            vacancies_processed += 1
    try:
        average_salary = int(sum_salaries / vacancies_processed)
    except ZeroDivisionError:
        average_salary = 0

    language_statistics = {
            "vacancies_found": vacancies_found,
            "vacancies_processed" : vacancies_processed,
            "average_salary" : average_salary
        }
    return language_statistics


def get_sj_statistics(secret_key: str, languages: list):
    general_statistics = {}
    for language in languages:
        total_vacancies = get_sj_vacancies(secret_key, language)
        language_statistics = get_sj_page_statistics(total_vacancies)
        general_statistics[language] = language_statistics
    return general_statistics
