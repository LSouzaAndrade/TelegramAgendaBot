from datetime import datetime


def validate_reservation(start_date: str, end_date: str) -> bool:

    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()

    condition_1 = end_date > start_date
    condition_2 = start_date > now

    return condition_1 and condition_2