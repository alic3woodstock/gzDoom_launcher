from dataPath import data_path


def connect_db():
    from dataConnect import SqliteDB
    return SqliteDB(data_path().db)


def select_grid_values(sql, params=""):
    data_con = connect_db()
    result = data_con.exec_sql(sql, params)
    values = []
    for r in result:
        values.append(r)
    data_con.close_connection()
    return values
