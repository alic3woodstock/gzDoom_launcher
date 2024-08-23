from functions import ConnectDb
from gameDef import GameDef


def delete_game_table():
    data_con = ConnectDb()
    data_con.StartTransaction()
    data_con.ExecSQL("""DROP TABLE IF EXISTS files;""")
    data_con.ExecSQL("""DROP TABLE IF EXISTS gamedef;""")
    data_con.ExecSQL("""DROP TABLE IF EXISTS groups""")
    data_con.Commit()
    data_con.CloseConnection()


def insert_game(game):
    data_con = ConnectDb()
    data_con.StartTransaction()
    sql = """INSERT INTO gamedef(name,tabindex,gamexec,modgroup,lastrunmod,iwad,cmdparams)
        VALUES (?,?,?,?,?,?,?);"""

    params = (game.name, game.tabId, game.exec, game.group.id,
              game.lastMod, game.iWad, game.cmdParams)

    data_con.ExecSQL(sql, params)

    game_ids = data_con.ExecSQL("""SELECT id FROM gamedef ORDER BY id DESC LIMIT 1;""")
    game_id = game_ids.fetchall()[0][0]

    sql = """INSERT INTO files(gameid,file) VALUES(?,?)"""
    for f in game.files:
        params = (game_id, f)
        data_con.ExecSQL(sql, params)

    data_con.Commit()
    data_con.CloseConnection()


def select_all_games():
    games = []
    data_con = ConnectDb()
    sql = """SELECT id, name, tabindex, gamexec, modgroup, lastrunmod, iwad, cmdparams 
        FROM gamedef
        ORDER BY tabindex,name"""

    game_data = data_con.ExecSQL(sql)
    for game in game_data:
        g = GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6], [], game[7])
        g.files = []
        file_data = data_con.ExecSQL("""SELECT file FROM files WHERE gameid = ?""", [game[0]])
        for f in file_data:
            g.files.append(f[0])
        games.append(g)
    data_con.CloseConnection()
    return games


def update_last_run_mod(game, mod):
    data_con = ConnectDb()
    data_con.StartTransaction()
    data_con.ExecSQL("""UPDATE gamedef SET lastrunmod=? WHERE id=?""", [mod.id, game.id])
    data_con.Commit()


def delete_game_by_id(game_id):
    data_con = ConnectDb()
    data_con.StartTransaction()
    data_con.ExecSQL("""DELETE FROM gamedef WHERE id=?""", [game_id])
    data_con.Commit()
    data_con.CloseConnection()


def select_game_by_id(game_id):
    data_con = ConnectDb()
    sql = """SELECT id, name, tabindex, gamexec, modgroup, 
        lastrunmod, iwad, cmdparams 
        FROM gamedef 
        WHERE id=?"""
    params = [game_id]
    game_data = data_con.ExecSQL(sql, params)
    game = game_data.fetchone()
    g = GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6], [], game[7])
    g.files = []
    file_data = data_con.ExecSQL("""SELECT file FROM files WHERE gameid = ?""", [game[0]])
    for f in file_data:
        g.files.append(f[0])
    data_con.CloseConnection()
    return g


def update_game(game, update_files=False):
    data_con = ConnectDb()
    data_con.StartTransaction()

    sql = """UPDATE gamedef SET name=?, tabindex=?, gamexec=?, modgroup=?, iwad=?, cmdparams=?
     WHERE id=?"""
    params = [game.name, game.tabId, game.exec, game.groupId, game.iWad, game.cmdParams, game.id]
    data_con.ExecSQL(sql, params)

    if update_files:
        sql = """DELETE FROM files WHERE gameid=?"""
        params = [game.id]
        data_con.ExecSQL(sql, params)
        sql = """INSERT INTO files(gameid,file) values(?,?)"""
        for f in game.files:
            params = [game.id, f]
            data_con.ExecSQL(sql, params)

    data_con.Commit()
    data_con.CloseConnection()


def update_wad(wad, mod_group):
    data_con = ConnectDb()
    data_con.StartTransaction()

    sql = """UPDATE gamedef SET iwad=? WHERE tabindex=1 AND modgroup=?"""
    params = [wad, mod_group]
    data_con.ExecSQL(sql, params)
    if mod_group == 2:
        data_con.ExecSQL("""DELETE FROM files WHERE file LIKE '%BLSMPTXT%' AND gameid IN 
        (SELECT id FROM gamedef g WHERE tabindex == 1)""")
    data_con.Commit()
