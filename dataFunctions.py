from functions import dbPath


def connect_db():
    from dataConnect import SqliteDB
    return SqliteDB(dbPath)


def select_grid_values(sql, params=""):
    dataCon = connect_db()
    result = dataCon.ExecSQL(sql, params)
    values = []
    for r in result:
        values.append(r)
    dataCon.CloseConnection()
    return values