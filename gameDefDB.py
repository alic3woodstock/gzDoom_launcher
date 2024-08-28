from dataFunctions import connect_db
from gameDef import GameDef


def delete_game_table():
    data_con = connect_db()
    data_con.start_transaction()
    data_con.exec_sql("""DROP TABLE IF EXISTS files;""")
    data_con.exec_sql("""DROP TABLE IF EXISTS gamedef;""")
    data_con.exec_sql("""DROP TABLE IF EXISTS groups""")
    data_con.commit()
    data_con.close_connection()


def insert_game(game):
    data_con = connect_db()
    data_con.start_transaction()
    sql = """INSERT INTO gamedef(name,tabindex,gamexec,modgroup,lastrunmod,iwad,cmdparams)
        VALUES (?,?,?,?,?,?,?);"""

    params = (game.name, game.tabId, game.exec, game.group.id,
              game.lastMod, game.iWad, game.cmdParams)

    data_con.exec_sql(sql, params)

    game_ids = data_con.exec_sql("""SELECT LAST_INSERT_ROWID();""")
    game_id = game_ids.fetchone()[0]

    sql = """INSERT INTO files(gameid,file) VALUES(?,?)"""
    for f in game.files:
        params = (game_id, f)
        data_con.exec_sql(sql, params)

    data_con.commit()
    data_con.close_connection()


def select_all_games():
    games = []
    data_con = connect_db()
    sql = """SELECT id, name, tabindex, gamexec, modgroup, lastrunmod, iwad, cmdparams 
        FROM gamedef
        ORDER BY tabindex,name"""

    game_data = data_con.exec_sql(sql)
    for game in game_data:
        g = GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6], [], game[7])
        g.files = []
        file_data = data_con.exec_sql("""SELECT file FROM files WHERE gameid = ?""", [game[0]])
        for f in file_data:
            g.files.append(f[0])
        games.append(g)
    data_con.close_connection()
    return games


def update_last_run_mod(game, mod_id):
    data_con = connect_db()
    data_con.start_transaction()
    data_con.exec_sql("""UPDATE gamedef SET lastrunmod=? WHERE id=?""", [mod_id, game.id])
    data_con.commit()


def delete_game_by_id(game_id):
    data_con = connect_db()
    data_con.start_transaction()
    data_con.exec_sql("""DELETE FROM gamedef WHERE id=?""", [game_id])
    data_con.commit()
    data_con.close_connection()


def select_game_by_id(game_id):
    data_con = connect_db()
    sql = """SELECT id, name, tabindex, gamexec, modgroup, 
        lastrunmod, iwad, cmdparams 
        FROM gamedef 
        WHERE id=?"""
    params = [game_id]
    game_data = data_con.exec_sql(sql, params)
    game = game_data.fetchone()
    g = GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6], [], game[7])
    g.files = []
    file_data = data_con.exec_sql("""SELECT file FROM files WHERE gameid = ?""", [game[0]])
    for f in file_data:
        g.files.append(f[0])
    data_con.close_connection()
    return g


def update_game(game, update_files=False):
    data_con = connect_db()
    data_con.start_transaction()

    sql = """UPDATE gamedef SET name=?, tabindex=?, gamexec=?, modgroup=?, iwad=?, cmdparams=?
     WHERE id=?"""
    params = [game.name, game.tabId, game.exec, game.groupId, game.iWad, game.cmdParams, game.id]
    data_con.exec_sql(sql, params)

    if update_files:
        sql = """DELETE FROM files WHERE gameid=?"""
        params = [game.id]
        data_con.exec_sql(sql, params)
        sql = """INSERT INTO files(gameid,file) values(?,?)"""
        for f in game.files:
            params = [game.id, f]
            data_con.exec_sql(sql, params)

    data_con.commit()
    data_con.close_connection()


def update_wad(wad, mod_group):
    data_con = connect_db()
    data_con.start_transaction()

    sql = """UPDATE gamedef SET iwad=? WHERE tabindex=1 AND modgroup=?"""
    params = [wad, mod_group]
    data_con.exec_sql(sql, params)
    if mod_group == 2:
        data_con.exec_sql("""DELETE FROM files WHERE file LIKE '%BLSMPTXT%' AND gameid IN 
        (SELECT id FROM gamedef g WHERE tabindex == 1)""")
    data_con.commit()
