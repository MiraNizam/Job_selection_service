import requests
from itertools import count
from collections import Counter


def get_hh_vacancies(url: str, languages: list) -> tuple:
    full_information = {}
    for language in languages:
        list_vacancies = []
        for page in count(1):
            payload = {
                "text": f"программист {language}",
                "area": "1", # Москва
                "period": 30,
                "only_with_salary": True,
                "currency": "RUR",
                "per_page": 100,
                "page": page
            }
            response = requests.get(f"{url}/vacancies", params=payload)
            response.raise_for_status()
            vacancies = response.json()
            list_vacancies.append(vacancies)
            full_information[language] = list_vacancies
            if page > int(vacancies["found"] / 100) or page >= 20:
                break
    return full_information


def get_hh_statistics(full_vacancies: dict) -> dict:
    total_statistics = {}
    for language, vacancies in full_vacancies.items():
        sum_salaries = 0
        vacancies_processed = 0
        try:
            average_salary = int(sum_salaries / vacancies_processed)
        except ZeroDivisionError as e:
            average_salary = 0

        for page_vacancies in vacancies:
            for vacancy in page_vacancies["items"]:
                expected_salary = predict_rub_salary_hh(vacancy["salary"])
                sum_salaries += expected_salary
                vacancies_processed += 1
                try:
                    average_salary = int(sum_salaries / vacancies_processed)
                except ZeroDivisionError as e:
                    average_salary = 0
            language_statistics = {
                "vacancies_found": page_vacancies["found"],
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
            }
            total_statistics[language] = language_statistics
    return total_statistics


def predict_rub_salary_hh(vacancy: dict) -> int:
    if vacancy["from"] is not None and vacancy["to"] is not None:
        return int((vacancy['from'] + vacancy["to"]) / 2)
    elif vacancy["from"] is not None and vacancy["to"] is None:
        return int(vacancy["from"]*1.2)
    elif vacancy["from"] is None and vacancy["to"] is not None:
        return int(vacancy["to"] * 0.8)
#

if __name__ == '__main__':
    url = "https://api.hh.ru"
    languages = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C", "Go", "TypeScript"]
    get_hh_vacancies = get_hh_vacancies(url, languages)
    hh_stat = get_hh_statistics(get_hh_vacancies)
    print(hh_stat)


