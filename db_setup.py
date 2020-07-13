# db_setup.py

import sqlite3
import os.path
from os import remove
from config import db_name

if(os.path.exists(db_name)):
    remove(db_name)


conn = sqlite3.connect('events.db')
curs = conn.cursor()

sql_query = """CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_time INTEGER NOT NULL,
    event_msg TEXT NOT NULL,
    repeat INTEGER NOT NULL,
    event_end INTEGER
    )"""
curs.execute(sql_query)
conn.commit()

conn.close()
