# db_setup.py

import sqlite3
import os.path
from os import remove
from config import db_name, table_name

if(os.path.exists(db_name)):
    remove(db_name)


conn = sqlite3.connect('events.db')
curs = conn.cursor()

sql_query = """CREATE TABLE {} (
    id INTEGER PRIMARY KEY,
    event_time INTEGER NOT NULL,
    event_id TEXT NOT NULL,
    repeat INTEGER NOT NULL,
    event_end INTEGER
    )""".format(table_name)
curs.execute(sql_query)

sql_query = """CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    event_id TEXT NOT NULL,
    message TEXT NOT NULL
    )"""
curs.execute(sql_query)

conn.commit()
conn.close()
