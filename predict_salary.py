def predict_salary(vacancy: dict or None, payment_from: str, payment_to: str, currency: str) -> int or None:
    if not vacancy:
        return None
    elif vacancy[payment_from] and vacancy[payment_to] and vacancy["currency"] == currency:
        return int((vacancy[payment_from] + vacancy[payment_to]) / 2)
    elif vacancy[payment_from] and not vacancy[payment_to] and vacancy["currency"] == currency:
        return int(vacancy[payment_from]*1.2)
    elif not vacancy[payment_from] and vacancy[payment_to] and vacancy["currency"] == currency:
        return int(vacancy[payment_to] * 0.8)
