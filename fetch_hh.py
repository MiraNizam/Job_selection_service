import requests
from itertools import count


def get_hh_vacancies(url: str, languages: list) -> tuple:
    for language in languages:
        total_vacancies = list()
        for page in count():
            payload = {
                "text": f"программист {language}",
                "area": "1",
                "period": 30,
                "only_with_salary": True,
                "currency": "RUR",
                "per_page": 50,
                "page": page
            }
            response = requests.get(f"{url}/vacancies", params=payload)
            response.raise_for_status()
            vacancies = response.json()
            total_vacancies.append(vacancies)

            if page >= vacancies["found"] / 50 or page >= 40:
                break
            yield language, total_vacancies


def get_hh_statistics(language: str, vacancies: dict) -> dict:
    summary_statistics = {}
    sum_salaries = 0
    vacancies_processed = 0

    for vacancy in vacancies["items"]:
        expected_salary = predict_rub_salary_hh(vacancy["salary"])
        sum_salaries += expected_salary
        vacancies_processed += 1

    try:
        average_salary = int(sum_salaries / vacancies_processed)
    except ZeroDivisionError as e:
        average_salary = 0

    language_statistics = {
        "vacancies_found": vacancies["found"],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    summary_statistics[language] = language_statistics
    return summary_statistics


def predict_rub_salary_hh(vacancy: dict) -> int:
    if vacancy["from"] is not None and vacancy["to"] is not None:
        return int((vacancy['from'] + vacancy["to"]) / 2)
    elif vacancy["from"] is not None and vacancy["to"] is None:
        return int(vacancy["from"]*1.2)
    elif vacancy["from"] is None and vacancy["to"] is not None:
        return int(vacancy["to"] * 0.8)


if __name__ == '__main__':
    url = "https://api.hh.ru"
    languages = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C", "Go", "TypeScript"]
    get_hh_vacancies(url, languages)
    for language, vacancies in get_hh_vacancies(url, languages):
        print(language, vacancies)
    #     print(get_hh_statistics(language, vacancies))

    #      пагинация
    # for page in count():
    #     payload = {
    #         "text": f"программист {language}",
    #         "area": "1",
    #         "period": 30,
    #         "only_with_salary": True,
    #         "currency": "RUR",
    #         "per_page": 10,
    #         "page": page
    #     }
    #     response = requests.get(f"{url}/vacancies", params=payload)
    #     response.raise_for_status()
    #     vacancies = response.json()
    #     url_pages.append(vacancies)
    #
    #     if page >= vacancies["found"] / 10 or page >= 100:
    #         break