from dataFunctions import connect_db
from gameTab import GameTabConfig


def update_game_tab(game_tab):
    if not (game_tab is None):
        data_con = connect_db()
        sql = """REPLACE INTO tabs(tabindex, label, enabled) 
         VALUES(?, ?, ?)"""
        data_con.start_transaction()

        for g in game_tab:
            params = [g.index,
                      g.name,
                      g.is_enabled]
            data_con.exec_sql(sql, params)

        # Clean unnamed tabs that aren't in any game
        sql = """DELETE FROM tabs WHERE tabindex NOT IN (SELECT DISTINCT(tabindex)
         FROM gamedef) AND label == '' AND enabled = false"""
        data_con.exec_sql(sql)

        data_con.commit()
        data_con.close_connection()


def select_all_game_tabs():
    data_con = connect_db()
    tab_configs = []
    sql = """SELECT tabindex, label, enabled FROM tabs WHERE tabindex >= 0 ORDER BY tabindex"""
    result = data_con.exec_sql(sql)
    for r in result:
        tab_configs.append(GameTabConfig(r[0], r[1], r[2]))
    data_con.close_connection()
    return tab_configs


def select_game_tab_by_id(tab_id):
    data_con = connect_db()
    sql = """SELECT tabindex, label, enabled FROM tabs WHERE tabindex = ?"""
    params = [tab_id]
    result = data_con.exec_sql(sql, params)
    r = result.fetchone()
    tab = GameTabConfig(r[0], r[1], r[2])
    data_con.close_connection()
    return tab
