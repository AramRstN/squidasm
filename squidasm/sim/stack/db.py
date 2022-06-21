import sqlite3

_conn = None


def create_connection(db_file=r"./db.sqlite"):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    """
    global _conn
    if _conn:
        return _conn
    try:
        _conn = sqlite3.connect(db_file)
        return _conn
    except Exception as e:
        print(e)

    return _conn


def create_fn_calls_table():
    create_table_sql = """ CREATE TABLE IF NOT EXISTS fn_calls (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        object_name text NOT NULL,
                                        attr_name text NOT NULL
                                    ); """
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute(create_table_sql)
    except Exception as e:
        print(e)
    finally:
        c.close()


def add_call_trace(object_name, attr_name):
    query = f"""INSERT INTO fn_calls (object_name, attr_name)
                VALUES('{object_name}','{attr_name}');"""
    if _conn is None:
        create_fn_calls_table()
    c = _conn.cursor()
    try:
        c.execute(query)
        _conn.commit()
    finally:
        c.close()


if __name__ == '__main__':
    # add_call_trace('hello', 'world')
    create_connection('../../../examples/stack/bqc/db.sqlite')
    c = _conn.cursor()
    for row in c.execute('SELECT * FROM fn_calls'):
        if 'client' in row[1]:
            print(row)

    c.close()
