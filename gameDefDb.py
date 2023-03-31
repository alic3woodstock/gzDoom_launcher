import dataConnect
import gameDef
import modGroup


class GameDefDb:
    _dataCon = None

    def GetDataCon(self):
        return self._dataCon

    def ConnectDb(self):
        self._dataCon = dataConnect.SqliteDB('games.sqlite3')
        return self._dataCon

    def CreateGameTable(self):
        dataCon = self.ConnectDb()

        dataCon.StartTransaction()
        dataCon.ExecSQL("""CREATE TABLE IF NOT EXISTS groups(
                id integer PRIMARY KEY AUTOINCREMENT,
                groupname text);
            """)

        dataCon.ExecSQL("""INSERT INTO groups(groupname) VALUES ('doom'),('heretic'),('hexen'),
                ('strife'),('other');
            """)

        dataCon.ExecSQL("""CREATE TABLE IF NOT EXISTS gamedef(
                id integer PRIMARY KEY AUTOINCREMENT,
                name text,
                tabindex integer NOT NULL,
                gamexec text,
                modgroup integer NOT NULL,
                lastrunmod integer NOT NULL,
                iwad text,
                cmdparams text NOT NULL DEFAULT '',
                FOREIGN KEY (modgroup) REFERENCES groups(id) ON DELETE NO ACTION);                
            """)
        #

        dataCon.ExecSQL("""CREATE TABLE IF NOT EXISTS files(
                id integer PRIMARY KEY AUTOINCREMENT,
                gameid integer,                        
                file text,
                FOREIGN KEY (gameid) REFERENCES gamedef(id) ON DELETE CASCADE);
            """)

        dataCon.Commit()
        dataCon.CloseConnection()

    def DeleteGameTable(self):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        dataCon.ExecSQL("""DROP TABLE IF EXISTS files;""")
        dataCon.ExecSQL("""DROP TABLE IF EXISTS gamedef;""")
        dataCon.ExecSQL("""DROP TABLE IF EXISTS groups""")
        dataCon.Commit()
        dataCon.CloseConnection()

    def InsertGame(self, game):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        sql = """INSERT INTO gamedef(name,tabindex,gamexec,modgroup,lastrunmod,iwad,cmdparams)
            VALUES (?,?,?,?,?,?,?);"""

        params = (game.GetItem().GetText(), game.GetTab(), game.GetExec(), game.GetGroup().GetGroupId(),
                  game.GetLastMod(), game.GetIWad(), game.GetCmdParams())

        dataCon.ExecSQL(sql, params)

        gameIds = dataCon.ExecSQL("""SELECT id FROM gamedef ORDER BY id DESC LIMIT 1;""")
        gameId = gameIds.fetchall()[0][0]

        sql = """INSERT INTO files(gameid,file) VALUES(?,?)"""
        for f in game.GetFiles():
            params = (gameId, f)
            dataCon.ExecSQL(sql, params)

        dataCon.Commit()
        dataCon.CloseConnection()

    def SelectAllGames(self):
        games = []

        dataCon = self.ConnectDb()
        gameData = dataCon.ExecSQL("""SELECT a.id, a.name, a.tabindex, a.gamexec, a.modgroup, a.lastrunmod, 
            a.iwad, b.groupname, a.cmdparams 
            FROM gamedef a LEFT JOIN groups b ON b.id = a.modgroup 
            ORDER BY tabindex,name;""")
        for game in gameData:
            g = gameDef.GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6], [], game[7],
                                game[8])
            g.SetFiles([])
            fileData = dataCon.ExecSQL("""SELECT file FROM files WHERE gameid = ?""", [game[0]])
            for f in fileData:
                g.GetFiles().append(f[0])
            games.append(g)
        dataCon.CloseConnection()
        return games

    def UpdateLastRunMod(self, game, mod):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        dataCon.ExecSQL("""UPDATE gamedef SET lastrunmod=? WHERE id=?""", [mod.GetItem().GetData(),
                                                                           game.GetItem().GetData()])
        dataCon.Commit()

    def DeleteGame(self, game):
        self.DeleteGameById(game.GetItem().GetData())

    def DeleteGameById(self, gameId):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        dataCon.ExecSQL("""DELETE FROM gamedef WHERE id=?""", [gameId])
        dataCon.Commit()
        dataCon.CloseConnection()

    def SelectGameById(self, gameId):
        dataCon = self.ConnectDb()
        gameData = dataCon.ExecSQL("""SELECT a.id, a.name, a.tabindex, a.gamexec, a.modgroup, a.lastrunmod, 
            a.iwad, b.groupname, a.cmdparams 
            FROM gamedef a LEFT JOIN groups b ON b.id = a.modgroup 
            WHERE a.id=?""", [gameId])
        game = gameData.fetchone()
        g = gameDef.GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6], [], game[7], game[8])
        g.SetFiles([])
        fileData = dataCon.ExecSQL("""SELECT file FROM files WHERE gameid = ?""", [game[0]])
        for f in fileData:
            g.GetFiles().append(f[0])
        dataCon.CloseConnection()
        return g

    def UpdateGame(self, game, updateFiles=False):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()

        sql = """UPDATE gamedef SET name=?, tabindex=?, gamexec=?, modgroup=?, iwad=?, cmdparams=?
         WHERE id=?"""
        params = [game.GetItem().GetText(), game.GetTab(), game.GetExec(), game.GetGroup().GetGroupId(), game.GetIWad(),
                  game.GetCmdParams(), game.GetItem().GetData()]
        dataCon.ExecSQL(sql, params)

        if updateFiles:
            sql = """DELETE FROM files WHERE gameid=?"""
            params = [game.GetItem().GetData()]
            dataCon.ExecSQL(sql, params)
            sql = """INSERT INTO files(gameid,file) values(?,?)"""
            for f in game.GetFiles():
                params = ([game.GetItem().GetData(), f])
                dataCon.ExecSQL(sql, params)

        dataCon.Commit()
        dataCon.CloseConnection()

    def SelectGroupById(self, groupId):
        dataCon = self.ConnectDb()

        sql = "SELECT groupname FROM groups where id=?"
        params = [groupId]

        groupData = dataCon.ExecSQL(sql, params)
        return groupData(0, 0)

    def SelectAllGroups(self):
        dataCon = self.ConnectDb()

        sql = "SELECT * FROM groups ORDER BY id"
        groupData = dataCon.ExecSQL(sql)

        groups = []
        for g in groupData:
            groups.append(modGroup.ModGroup(g[0], g[1]))
        dataCon.CloseConnection()

        return groups

    def UpdateWad(self, wad, modgroup):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()

        sql = """UPDATE gamedef SET iwad=? WHERE tabindex=1 AND modgroup=?"""
        params = [wad, modgroup]
        dataCon.ExecSQL(sql, params)
        if modgroup == 2:
            dataCon.ExecSQL("""DELETE FROM files WHERE file LIKE '%BLSMPTXT%'""")
        dataCon.Commit()

    def UpdateDatabase(self):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()

        sql = """SELECT sql FROM sqlite_master WHERE tbl_name = ?"""
        params = ["gamedef"]
        text = dataCon.ExecSQL(sql, params)
        for t in text:
            sql = t[0]

        if sql.lower().find("cmdparams") < 0:
            sql = """ALTER TABLE gamedef ADD COLUMN cmdparams text NOT NULL DEFAULT ''"""
            dataCon.ExecSQL(sql)

        dataCon.Commit()
