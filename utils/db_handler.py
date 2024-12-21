import sqlite3


db_name = 'messages.db'

def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        message_id INTEGER PRIMARY KEY,
                        reply_to_message_id INTEGER DEFAULT NULL,
                        content TEXT DEFAULT NULL)''')
    conn.commit()
    conn.close()

def save_message(message_id, reply_to_message_id, content):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO messages (message_id, reply_to_message_id, content) VALUES (?, ?, ?)', 
                        (message_id, reply_to_message_id, content))
        conn.commit()

    except sqlite3.Error as e:
        print(f'Erro ao salvar mensagem no banco de dados: {e}')
    finally:
        conn.close()
