import requests
from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
LANGUAGES = env.list("LANGUAGES")
URL = "https://api.superjob.ru/2.0/vacancies/"


def get_sj_vacancies(url: str, secret_key: str, language: str) -> list:
    headers = {"X-Api-App-Id": secret_key}
    total_vacancies = []
    for page in range(5):
        payload = {"town": "Москва", "keyword": f"программист {language}", "page": page, "count": 100}
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        vacancies = response.json()
        total_vacancies.append(vacancies)
        if page > vacancies["total"] / 100:
            break
    return total_vacancies


def predict_rub_salary_sj(vacancy: dict or None) -> int or None:
    if vacancy is None:
        return None
    elif vacancy["payment_from"] != 0 and vacancy["payment_to"] != 0 and vacancy["currency"] == "rub":
        return int((vacancy["payment_from"] + vacancy["payment_to"] / 2))
    elif vacancy["payment_from"] != 0 and vacancy["payment_to"] == 0 and vacancy["currency"] == "rub":
        return int(vacancy["payment_from"] * 1.2)
    elif vacancy["payment_from"] == 0 and vacancy["payment_to"] != 0 and vacancy["currency"] == "rub":
        return int(vacancy["payment_to"] * 0.8)


def get_sj_statistics(total_vacancies: list) -> dict:
    sum_salaries = 0
    vacancies_processed = 0
    vacancies_found = 0
    average_salary = 0
    for vacancies in total_vacancies:
        vacancies_found = vacancies["total"]
        for vacancy in vacancies["objects"]:
            expected_salary = predict_rub_salary_sj(vacancy)
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
            "vacancies_processed" : vacancies_processed,
            "average_salary" : average_salary
        }
    return language_statistics


def main():
    general_statistics = {}
    for language in LANGUAGES:
        total_vacancies = get_sj_vacancies(URL, SECRET_KEY, language)
        language_statistics = get_sj_statistics(total_vacancies)
        general_statistics[language] = language_statistics
    return general_statistics


if __name__ == '__main__':
    main()