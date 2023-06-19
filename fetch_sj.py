import requests
from itertools import count
from environs import Env

env = Env()
env.read_env()


def get_sj_vacancies(url: str, secret_key: str, languages: list) -> tuple:
    headers = {"X-Api-App-Id": secret_key}
    # total_vacancies = list()
    for language in languages:
        payload = {"town":"Москва", "keyword": f"программист {language}"}
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        vacancies = response.json()

    # if page >= vacancies["total"] / 100 or page >= 5:
    #     break

        yield language, vacancies


def get_sj_statistics(language: str, vacancies: dict) -> dict:
    summary_statistics = {}
    sum_salaries = 0
    vacancies_processed = 0

    for vacancy in vacancies["objects"]:
        expected_salary = predict_rub_salary_sj(vacancy)
        if expected_salary is not None:
            sum_salaries += expected_salary
            vacancies_processed += 1

    try:
        average_salary = int(sum_salaries / vacancies_processed)
    except ZeroDivisionError as e:
        average_salary = 0

    language_statistics = {
            "vacancies_found": vacancies["total"],
            "vacancies_processed" : vacancies_processed,
            "average_salary" : average_salary
        }
    summary_statistics[language] = language_statistics
    return summary_statistics


def predict_rub_salary_sj(vacancy: dict) -> int or None:
    if vacancy["payment_from"] != 0 and vacancy["payment_to"] != 0 and vacancy["currency"] == "rub":
        return int((vacancy["payment_from"] + vacancy["payment_to"] / 2))
    elif vacancy["payment_from"] != 0 and vacancy["payment_to"] == 0 and vacancy["currency"] == "rub":
        return int(vacancy["payment_from"] * 1.2)
    elif vacancy["payment_from"] == 0 and vacancy["payment_to"] != 0 and vacancy["currency"] == "rub":
        return int(vacancy["payment_to"] * 0.8)
    else:
        return None


if __name__ == '__main__':
    SECRET_KEY = env.str("SECRET_KEY")
    url = "https://api.superjob.ru/2.0/vacancies/"
    languages = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C", "Go", "TypeScript"]
    for language, vacancies in get_sj_vacancies(url, SECRET_KEY, languages):
        print(get_sj_statistics(language, vacancies))