import requests
from environs import Env

env = Env()
env.read_env()

LANGUAGES = env.list("LANGUAGES")
URL = "https://api.hh.ru"


def get_hh_vacancies(url: str, language: str) -> list:
    total_vacancies = []
    for page in range(20):
        payload = {
            "text": f"программист {language}",
            "area": "1", # Москва
            "period": 30,
            "currency": "RUR",
            "per_page": 100,
            "page": page
        }
        response = requests.get(f"{url}/vacancies", params=payload)
        response.raise_for_status()
        vacancies = response.json()
        total_vacancies.append(vacancies)
        if page > int(vacancies["found"] / 100):
            break
    return total_vacancies


def predict_salary_hh(vacancy: dict or None) -> int or None:
    if vacancy is None:
        return None
    elif vacancy["from"] is not None and vacancy["to"] is not None:
        return int((vacancy['from'] + vacancy["to"]) / 2)
    elif vacancy["from"] is not None and vacancy["to"] is None:
        return int(vacancy["from"]*1.2)
    elif vacancy["from"] is None and vacancy["to"] is not None:
        return int(vacancy["to"] * 0.8)


def get_hh_statistics(total_vacancies: list) -> dict:
    sum_salaries = 0
    vacancies_processed = 0
    vacancies_found = 0
    average_salary = 0
    for page_vacancies in total_vacancies:
        vacancies_found = page_vacancies["found"]
        for vacancy in page_vacancies["items"]:
            expected_salary = predict_salary_hh(vacancy["salary"])
            if expected_salary is None:
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
    general_statistics = {}
    for language in LANGUAGES:
        total_vacancies = get_hh_vacancies(URL, language)
        language_statistics = get_hh_statistics(total_vacancies)
        general_statistics[language] = language_statistics
    return general_statistics
