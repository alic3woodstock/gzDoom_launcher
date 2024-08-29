from dataFunctions import connect_db


def update_gzdoom_version(version, filehash):
    write_config('gzdversion', version, 'text')
    write_config('gzdhash', filehash, 'text')


def check_gzdoom_version(version, filehash):
    data_version = read_config('gzdversion', 'text')
    data_hash = read_config('gzdhash', 'text')
    if data_version == version and data_hash == filehash:
        return True
    else:
        return False


def write_config(param="", value=None, value_type="text"):
    data_con = connect_db()
    sql = """REPLACE INTO config (param,"""
    if value_type == "num":
        sql += """numvalue)"""
        if value == "":
            value = 0
    elif value_type == "bool":
        sql += """boolvalue)"""
        if value == "":
            value = False
    else:
        sql += """txtvalue)"""

    sql += """ VALUES(?,?)"""
    params = [param, value]
    data_con.start_transaction()
    data_con.exec_sql(sql, params)
    data_con.commit()
    data_con.close_connection()


def read_config(param="", valuetype="text"):
    data_con = connect_db()
    if valuetype == "num":
        sql = """SELECT numvalue"""
        default_value = 0
    elif valuetype == "bool":
        sql = """SELECT boolvalue"""
        default_value = False
    else:
        sql = """SELECT txtvalue"""
        default_value = ""

    sql += """ FROM config WHERE param = ?"""
    params = [param]
    result = data_con.exec_sql(sql, params)
    return_value = default_value
    for r in result:
        return_value = r[0]
        break
    data_con.close_connection()
    return return_value
