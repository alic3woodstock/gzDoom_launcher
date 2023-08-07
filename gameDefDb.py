import dataConnect
import functions
import gameDef
import modGroup
import gameTabConfig

CREATE_CONFIG = """CREATE TABLE IF NOT EXISTS config(
                    id INTEGER PRIMARY KEY,
                    param TEXT UNIQUE,
                    txtvalue TEXT,
                    numvalue INTEGER,
                    boolvalue BOOLEAN)"""

CREATE_TABS = """CREATE TABLE IF NOT EXISTS tabs(
            tabindex INTEGER PRIMARY KEY,
            label TEXT NOT NULL DEFAULT '',
            enabled BOOLEAN NOT NULL DEFAULT true)"""

CREATE_GAMEDEF = """CREATE TABLE IF NOT EXISTS gamedef(
                id integer PRIMARY KEY AUTOINCREMENT,
                name text,
                tabindex integer NOT NULL,
                gamexec text,
                modgroup integer NOT NULL,
                lastrunmod integer NOT NULL,
                iwad text,
                cmdparams text NOT NULL DEFAULT '',
                FOREIGN KEY (modgroup) REFERENCES groups(id) ON DELETE NO ACTION,
                FOREIGN KEY (tabindex) REFERENCES tabs(tabindex) ON DELETE NO ACTION ON UPDATE CASCADE);                
            """


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

        sql = CREATE_TABS
        dataCon.ExecSQL(sql)

        sql = """INSERT or IGNORE INTO tabs(tabindex, label, enabled)
            VALUES (?,?,?)"""
        params = [-1, "Mods", True]
        dataCon.ExecSQL(sql, params)
        params = [0, "Games", True]
        dataCon.ExecSQL(sql, params)
        params = [1, "Maps", True]
        dataCon.ExecSQL(sql, params)

        dataCon.ExecSQL(CREATE_GAMEDEF)

        dataCon.ExecSQL("""CREATE TABLE IF NOT EXISTS files(
                id integer PRIMARY KEY AUTOINCREMENT,
                gameid integer,                        
                file text,
                FOREIGN KEY (gameid) REFERENCES gamedef(id) ON DELETE CASCADE);
            """)

        dataCon.ExecSQL(CREATE_CONFIG)

        sql = """REPLACE INTO config (param, numvalue)
            VALUES ('dbversion', ?)"""
        params = [10100]
        dataCon.ExecSQL(sql, params)

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
        dbVersion = self.CheckDbVersion()

        dataCon.StartTransaction()
        sql = """SELECT sql FROM sqlite_master WHERE tbl_name = ?"""
        params = ["config"]
        text = dataCon.ExecSQL(sql, params)
        strTable = ""
        for t in text:
            if t[0]:
                strTable = t[0]

        if strTable.lower().find("config") < 0:
            sql = """SELECT sql FROM sqlite_master WHERE tbl_name = ?"""
            params = ["gamedef"]
            text = dataCon.ExecSQL(sql, params)
            for t in text:
                sql = t[0]

            if sql.lower().find("cmdparams") < 0:
                sql2 = """ALTER TABLE gamedef ADD COLUMN cmdparams text NOT NULL DEFAULT ''"""
                dataCon.ExecSQL(sql2)

            if sql.lower().find("ismod") < 0:
                sql2 = """ALTER TABLE gamedef ADD COLUMN ismod BOOLEAN NOT NULL DEFAULT false"""
                dataCon.ExecSQL(sql2)
                sql2 = """UPDATE gamedef SET ismod = true WHERE tabindex = 2"""
                dataCon.ExecSQL(sql2)
                sql2 = """UPDATE gamedef SET tabindex = -1 WHERE ismod = true"""
                dataCon.ExecSQL(sql2)
                sql2 = """ALTER TABLE gamedef DROP COLUMN ismod"""
                dataCon.ExecSQL(sql2)

            sql = """CREATE TABLE IF NOT EXISTS gzdoom_version(
                id INTEGER PRIMARY KEY,
                version text,
                sha256 text)"""
            dataCon.ExecSQL(sql)

            dataCon.ExecSQL(CREATE_CONFIG)

        if dbVersion < 10100:
            dataCon.ExecSQL(CREATE_TABS)

            sql = """REPLACE INTO tabs(tabindex, label, enabled)
                VALUES (?,?,?)"""
            params = [-1, "Mods", True]
            dataCon.ExecSQL(sql, params)
            params = [0, "Games", True]
            dataCon.ExecSQL(sql, params)
            params = [1, "Maps", True]
            dataCon.ExecSQL(sql, params)

            sql = """UPDATE gamedef SET tabindex=0 WHERE id IN (
                SELECT DISTINCT g.id FROM gamedef g LEFT JOIN tabs t on t.tabindex = g.tabindex WHERE 
                t.tabindex IS NULL)"""
            dataCon.ExecSQL(sql)

            dataCon.ExecSQL("""ALTER TABLE gamedef RENAME TO gamedef_old""")
            dataCon.ExecSQL(CREATE_GAMEDEF)
            dataCon.ExecSQL("""INSERT INTO gamedef SELECT * FROM gamedef_old""")
            dataCon.ExecSQL("""DROP TABLE gamedef_old""")

        sql = """REPLACE INTO config (param, numvalue)
            VALUES (?, ?)"""
        params = ['dbversion', functions.versionNumber()]
        dataCon.ExecSQL(sql, params)
        dataCon.Commit()

        dataCon.CloseConnection()


    def UpdateGzdoomVersion(self, version, filehash):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        sql = """REPLACE INTO gzdoom_version(id, version, sha256)
        VALUES (?,?,?)"""
        params = [1, version, filehash]
        dataCon.ExecSQL(sql, params)
        dataCon.Commit()

    def CheckGzDoomVersion(self, version, filehash):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        dataVersion = '0'
        dataHash = '0'
        sql = """SELECT * FROM gzdoom_version WHERE id = ?"""
        params = [1]
        fileData = dataCon.ExecSQL(sql, params)
        for data in fileData:
            dataVersion = data[1]
            dataHash = data[2]

        if dataVersion == version and dataHash == filehash:
            return True
        else:
            return False

    def CheckDbVersion(self):
        dataCon = self.ConnectDb()
        sql = """SELECT sql FROM sqlite_master WHERE tbl_name = ?"""
        params = ["config"]
        text = dataCon.ExecSQL(sql, params)
        strTable = ""
        for t in text:
            if t[0]:
                strTable = t[0]
        if strTable.lower().find("config") < 0:
            return 0
        else:
            sql = """SELECT numvalue FROM config WHERE param = 'dbversion'"""
            versionData = dataCon.ExecSQL(sql)
            for v in versionData:
                version = v[0]

            return int(version)

    def ReadConfig(self, param = "", valuetype ="text"):
        dataCon = self.ConnectDb()
        if valuetype == "num":
            sql = """SELECT numvalue"""
            defaultValue = 0
        elif valuetype == "bool":
            sql = """SELECT boolvalue"""
            defaultValue = False
        else:
            sql = """SELECT textvalue"""
            defaultValue = ""
            
        sql += """ FROM config WHERE param = ?"""
        params = [param]
        result = dataCon.ExecSQL(sql, params)
        returnValue = defaultValue
        for r in result:
            returnValue = r[0]
            break
        dataCon.CloseConnection()
        return  returnValue


    def WriteConfig(self, param = "", value = "", valuetype = "text"):
        dataCon = self.ConnectDb()
        sql = """REPLACE INTO config (param,"""
        if valuetype == "num":
            sql += """numvalue)"""
            if (value == ""):
                value = 0
        elif valuetype == "bool":
            sql += """boolvalue)"""
            if (value == ""):
                value = False
        else:
            sql += """textvalue)"""

        sql += """ VALUES(?,?)"""
        params = [param, value]
        dataCon.StartTransaction()
        dataCon.ExecSQL(sql, params)
        dataCon.Commit()
        dataCon.CloseConnection()

    def SelctGameTabConfigByIndex(self, tabIndex):
        sql = """SELECT label, enabled FROM tabs WHERE tabindex = ?"""
        params = [tabIndex]
        dataCon = self.ConnectDb()
        tabs = dataCon.ExecSQL(sql, params)
        tabConfig = gameTabConfig.GameTabConfig(tabIndex,"",False)
        for t in tabs:
            tabConfig.SetName(t[0])
            tabConfig.SetEnabled(t[1])

        dataCon.CloseConnection()

        return tabConfig

    def UpdateGameTabConfig(self, gameTabConfig):
        if not (gameTabConfig is None):
            dataCon = self.ConnectDb()
            sql = """REPLACE INTO tabs(tabindex, label, enabled) 
             VALUES(?, ?, ?)"""
            dataCon.StartTransaction()

            try:
                for g in gameTabConfig:
                    params = [g.GetIndex(),
                              g.GetName(),
                              g.IsEnabled()]
                    dataCon.ExecSQL(sql, params)
            except TypeError:
                params = [gameTabConfig.GetIndex(),
                          gameTabConfig.GetName(),
                          gameTabConfig.IsEnabled()]
                dataCon.ExecSQL(sql, params)

            dataCon.Commit()
            dataCon.CloseConnection()

    def SelectAllGameTabConfigs(self):
        dataCon = self.ConnectDb()
        tabConfigs = []
        sql = """SELECT tabindex, label, enabled FROM tabs WHERE tabindex >= 0 ORDER BY tabindex"""
        result = dataCon.ExecSQL(sql)
        for r in result:
            tabConfigs.append(gameTabConfig.GameTabConfig(r[0], r[1], r[2]))
        dataCon.CloseConnection()
        return  tabConfigs