import sqlite3


db_name = 'reservations.db'

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
    return result is not None

@with_database(db_name)
def insert_reservation(cursor, reservation_object, start_datetime, end_datetime):
    cursor.execute('''INSERT INTO reservations 
                    (reservation_object, start_datetime, end_datetime)
                    VALUES (?, ?, ?)''',
                    (reservation_object, start_datetime, end_datetime))
    return True
