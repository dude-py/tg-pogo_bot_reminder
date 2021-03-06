# event.py
import sqlite3 as lite
import config

db_name = config.db_name
table = config.table_name


def execute(query):
    result = None
    try:
        con = lite.connect(db_name)
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        con.commit()
    except lite.DatabaseError as err:
        print("DatabaseError: %s" % (err))
    finally:
        con.close()
        print(query)
        return result


def create(table, schema, *values):
    """ add new event to database """
    # if(len(values) != 4):
    #     raise ValueError("can't create new event. wrong arguments")

    # for database
    sql_query = "INSERT INTO {} {} VALUES {}".format(table, schema, values)
    sql_query = sql_query.replace('[', '(').replace(']', ')')
    execute(sql_query)


def read(table, cols='*', event_id=None):
    """ read all data from db """
    sql_query = "SELECT %s FROM %s" % (cols, table)

    if event_id is not None:
        sql_query += " WHERE event_id='{}'".format(event_id)

    result = execute(sql_query)
    return result


def update(id, key, value):
    """ save new :value in :key where :id """
    if(type(value) is str):
        value = '"' + value + '"'

    if(key in config.schema):
        sql_query = "UPDATE {} SET {} = {} WHERE id = {}"\
                .format(table, key, value, id)
        execute(sql_query)
    else:
        print("KeyERROR")


def delete(_id):
    """ delete event with :id """
    sql_query = "DELETE FROM %s WHERE id=%i" % (table, _id)
    execute(sql_query)
