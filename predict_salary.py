def predict_salary(from_salary: int or None, to_salary: int or None) -> int:
    if from_salary and to_salary:
        return int((from_salary + to_salary) / 2)
    elif from_salary and not to_salary:
        return int(from_salary*1.2)
    elif not from_salary and to_salary:
        return int(to_salary * 0.8)