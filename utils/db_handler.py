import sqlite3
from datetime import datetime


db_name = 'reservations.db'

def validate_data(start_datetime: str, end_datetime: str) -> bool:
    start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    condition_1 = end_datetime > start_datetime
    result = {'success': 'The data is valid.'}
    if not condition_1:
        result = {'invalid_date': 'The start date must be greater than the end date.'}
    condition_2 = start_datetime > now
    if not condition_2:
        result = {'invalid_date': 'Now is ' + now.strftime('%Y-%m-%d %H:%M:%S') + '. The start date must be greater than now.'}
    return result

def with_database(db_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                result = func(cursor, *args, **kwargs)
                conn.commit()
                return result
            except sqlite3.Error as e:
                print(f"Erro ao executar a função no banco de dados: {e}")
            finally:
                if conn:
                    conn.close()
        return wrapper
    return decorator

@with_database(db_name)
def init_db(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        reservation_object TEXT NOT NULL,
                        start_datetime TEXT NOT NULL,
                        end_datetime TEXT NOT NULL)''')

@with_database(db_name)
def check_reservation_availability(cursor, reservation_object, start_datetime, end_datetime):
    data_validation = validate_data(start_datetime, end_datetime)
    if 'success' in data_validation.keys():
        data_validation = {'success': 'The reservation is available.'}
        cursor.execute('''SELECT 1 
                            FROM reservations
                            WHERE reservation_object = ?
                                AND (
                                    (start_datetime < ? AND end_datetime > ?)
                                    OR (start_datetime < ? AND end_datetime > ?)
                                    OR (start_datetime >= ? AND end_datetime <= ?)
                                )
                            LIMIT 1''',
                            (reservation_object, start_datetime, start_datetime, 
                                end_datetime, end_datetime, start_datetime, end_datetime))
        result = cursor.fetchone()
        if result:
            data_validation = {'error': 'There is a conflict with an existing reservation.'}         
    return data_validation

@with_database(db_name)
def insert_reservation(cursor, reservation_object, start_datetime, end_datetime):
    validation_status = check_reservation_availability(reservation_object, start_datetime, end_datetime)
    if 'success' in validation_status.keys():
        cursor.execute('''INSERT INTO reservations 
                        (reservation_object, start_datetime, end_datetime)
                        VALUES (?, ?, ?)''',
                        (reservation_object, start_datetime, end_datetime))
        return {'success': 'The reservation was successfully inserted.'}
    else:
        return validation_status
    
