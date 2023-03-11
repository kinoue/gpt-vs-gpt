import os
import sqlite3 as sl
from collections import OrderedDict

DB_FILE_NAME = 'gpt-vs-gpt.db'
def init_db():
    with sl.connect(DB_FILE_NAME) as connection:
        connection.execute("""
            CREATE TABLE dialogues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                stance TEXT,
                num_turns INTEGER,
                temperature REAL,
                views INTEGER
            );
        """)

        connection.execute("""
            CREATE TABLE statements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dialogue_id INTEGER,
                statement TEXT
            );
        """)

def add_dialogue(topic: str, stance: str, num_turns: int, temperature: float, statements: list):
    with sl.connect('gpt-vs-gpt.db') as connection:
        cursor = connection.cursor() 
        try:
            cursor.execute(
                "INSERT INTO dialogues VALUES (?, ?, ?, ?, ?, 1);",
                [None, topic, stance, num_turns, temperature]
            )
            dialogue_id = cursor.lastrowid
            for statement in statements:
                cursor.execute(
                    "INSERT INTO statements VALUES (?, ?, ?);",
                    [None, dialogue_id, statement]
                )
        finally:
            cursor.close()

def get_dialogues():
    with sl.connect('gpt-vs-gpt.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM dialogues ORDER BY id"
            )
            dialogues = OrderedDict()
            for row in cursor.fetchall():
                dialogues[row[0]] = {
                    "id": row[0],
                    "topic": row[1],
                    "stance": row[2],
                    "num_turns": row[3],
                    "temperature": row[4],
                    "views": row[5]
                }
            return dialogues
            '''
            alternative, not used
            return [
                {
                    "id": row[0],
                    "topic": row[1],
                    "stance": row[2],
                    "num_turns": row[3],
                    "temperature": row[4]
                }
                for row in cursor.fetchall()
            ]
            '''
        finally:
            cursor.close()
    return None

def get_statements(dialogue_id=None):
    with sl.connect('gpt-vs-gpt.db') as connection:
        cursor = connection.cursor()
        try:
            if dialogue_id:
                cursor.execute(
                    "SELECT * FROM statements WHERE dialogue_id = ? ORDER BY id",
                    [dialogue_id]
                )
            else:
                cursor.execute("SELECT * FROM statements ORDER BY id")
            statements = OrderedDict()
            for row in cursor.fetchall():
                statements[row[0]] = {
                    "id": row[0],
                    "dialogue_id": row[1],
                    "statement": row[2]
                }
            return statements

            '''
            alternative return, not used
            return [
                {
                    "id": row[0],
                    "dialogue_id": row[1],
                    "statement": row[2]
                }
                for row in cursor.fetchall()
            ]
            '''
        finally:
            cursor.close()
    return None

def increment_dialogue_view(dialogue_id):
    with sl.connect('gpt-vs-gpt.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE dialogues SET views = views + 1 WHERE id = ?",
                [dialogue_id]
            )
        finally:
            cursor.close()

if not os.path.exists('gpt-vs-gpt.db'):
    init_db()


if __name__ == '__main__':
    print('initializing the dabase...')
    init_db()