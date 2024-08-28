from dataFunctions import connect_db


def select_group_by_id(group_id):
    from modGroup import ModGroup
    data_con = connect_db()
    sql = """SELECT id, groupname FROM groups WHERE id=?"""
    params = [group_id]
    group_data = data_con.exec_sql(sql, params)
    g = group_data.fetchone()
    group = ModGroup(g[0], g[1])
    return group


def select_all_groups():
    from modGroup import ModGroup
    data_con = connect_db()

    sql = "SELECT * FROM groups ORDER BY id"
    group_data = data_con.exec_sql(sql)

    groups = []
    for g in group_data:
        groups.append(ModGroup(g[0], g[1]))
    data_con.close_connection()

    return groups
