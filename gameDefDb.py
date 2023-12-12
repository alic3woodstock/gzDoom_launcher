import dataConnect
import functions
import gameDef
import modGroup
import gameTabConfig

from url import Url

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

CREATE_DOWNLOADLIST = """CREATE TABLE IF NOT EXISTS downloadlist(
                id integer PRIMARY KEY AUTOINCREMENT,
                url text ,
                filename text UNIQUE)
            """


class GameDefDb:
    _dataCon = None

    def GetDataCon(self):
        return self._dataCon

    def ConnectDb(self):
        self._dataCon = dataConnect.SqliteDB(functions.dbPath)
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
        params = [20000]
        dataCon.ExecSQL(sql, params)

        dataCon.ExecSQL(CREATE_DOWNLOADLIST)
        self.InsertDefaultUrls(dataCon)

        dataCon.Commit()
        dataCon.CloseConnection()

        self.WriteConfig("checkupdate", True, "bool")

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

        params = (game.name, game.tab, game.exec, game.group.GetGroupId(),
                  game.lastMod, game.iWad, game.cmdParams)

        dataCon.ExecSQL(sql, params)

        gameIds = dataCon.ExecSQL("""SELECT id FROM gamedef ORDER BY id DESC LIMIT 1;""")
        gameId = gameIds.fetchall()[0][0]

        sql = """INSERT INTO files(gameid,file) VALUES(?,?)"""
        for f in game.files:
            params = (gameId, f)
            dataCon.ExecSQL(sql, params)

        dataCon.Commit()
        dataCon.CloseConnection()

    def SelectAllGames(self, desc=False):
        games = []

        dataCon = self.ConnectDb()
        sql = """SELECT a.id, a.name, a.tabindex, a.gamexec, a.modgroup, a.lastrunmod, 
            a.iwad, b.groupname, a.cmdparams 
            FROM gamedef a LEFT JOIN groups b ON b.id = a.modgroup 
            ORDER BY tabindex,name"""
        if desc:
            sql += """ DESC"""

        gameData = dataCon.ExecSQL(sql)
        for game in gameData:
            g = gameDef.GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6], [], game[7],
                                game[8])
            g.files = []
            fileData = dataCon.ExecSQL("""SELECT file FROM files WHERE gameid = ?""", [game[0]])
            for f in fileData:
                g.files.append(f[0])
            games.append(g)
        dataCon.CloseConnection()
        return games

    def UpdateLastRunMod(self, game, mod):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        dataCon.ExecSQL("""UPDATE gamedef SET lastrunmod=? WHERE id=?""", [mod.id, game.id])
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
        params = [game.GetItem().GetText(), game.GetTab(), game.GetExec(), game.group.GetGroupId(), game.GetIWad(),
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

        if dbVersion < 20000:
            dataCon.ExecSQL(CREATE_DOWNLOADLIST)
            self.InsertDefaultUrls()

        sql = """REPLACE INTO config (param, numvalue)
            VALUES (?, ?)"""
        params = ['dbversion', functions.versionNumber()]
        dataCon.ExecSQL(sql, params)
        dataCon.Commit()

        dataCon.CloseConnection()


    def UpdateGzdoomVersion(self, version, filehash):
        self.WriteConfig('gzdversion', version, 'text')
        self.WriteConfig('gzdhash', filehash, 'text')

    def CheckGzDoomVersion(self, version, filehash):
        dataVersion = self.ReadConfig('gzdversion','text')
        dataHash = self.ReadConfig('gzdhash','text')
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
            sql = """SELECT txtvalue"""
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
            sql += """txtvalue)"""

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

            for g in gameTabConfig:
                params = [g.GetIndex(),
                          g.GetName(),
                          g.IsEnabled()]
                dataCon.ExecSQL(sql, params)

            #Clean unnamed tabs that aren't in any game
            sql = """DELETE FROM tabs WHERE tabindex NOT IN (SELECT DISTINCT(tabindex)
             FROM gamedef) AND label == '' AND enabled = false"""
            dataCon.ExecSQL(sql)

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

    def InsertDefaultUrls(self, dataCon = None):
        if dataCon:
            commit = False
        else:
            dataCon = self.ConnectDb()
            dataCon.StartTransaction()
            commit = True

        sql = """REPLACE INTO downloadlist (url, filename) VALUES (?, ?) """

        # Blasphemer
        params = ["https://github.com/Blasphemer/blasphemer/releases/download/v0.1.7/blasphem-0.1.7.zip",
                  "blasphem.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://github.com/Blasphemer/blasphemer/releases/download/v0.1.7/blasphemer-texture-pack.zip",
                  "blasphemer-texture-pack.zip"]
        dataCon.ExecSQL(sql, params)

        # Freedoom
        params = ["https://github.com/freedoom/freedoom/releases/download/v0.12.1/freedoom-0.12.1.zip", "freedoom.zip"]
        dataCon.ExecSQL(sql, params)

        # 150skins
        params = ["https://awxdeveloper.edu.eu.org/downloads/150skins.zip", "150skins.zip"] #my personal wordpress site
        dataCon.ExecSQL(sql, params)

        # Beautiful Doom
        params = ["https://github.com/jekyllgrim/Beautiful-Doom/releases/download/7.1.6/Beautiful_Doom_716.pk3",
                  "Beautiful_Doom.pk3"]
        dataCon.ExecSQL(sql, params)

        # Brutal Doom
        params = ["https://github.com/BLOODWOLF333/Brutal-Doom-Community-Expansion/releases/"
                  "download/V21.11.2/brutalv21.11.2.pk3", "brutal.pk3"]
        dataCon.ExecSQL(sql, params)

        #maps
        params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/av.zip", "av.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/aaliens.zip", "aliens.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e1.zip", "btsx_e1.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e2.zip", "btsx_e2.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://www.dropbox.com/s/vi47z1a4e4c4980/Sunder%202407.zip?dl=1", "sunder.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/eviternity.zip", "eviternity.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://eviternity-dl-us.dfdoom.com/Eviternity-II.zip", "Eviternity-II.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/gd.zip", "gd.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/themes/hr/hr.zip", "hr.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/themes/hr/hr2final.zip", "hr2final.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/heretic/Ports/htchest.zip", "htchest.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/themes/mm/mm_allup.zip", "mm_allup.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/themes/mm/mm2.zip", "mm2.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/pl2.zip", "pl2.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/scythe.zip", "scythe.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/scythe2.zip", "scythe2.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/s-u/scythex.zip", "scythex.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/sunlust.zip", "sunlust.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/heretic/s-u/unbeliev.zip", "unbeliev.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/valiant.zip", "valiant.zip"]
        dataCon.ExecSQL(sql, params)
        params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/zof.zip", "zof.zip"]
        dataCon.ExecSQL(sql, params)

        if commit:
            dataCon.Commit()
            dataCon.CloseConnection()

    def SelectDefaultUrls(self):
        dataCon = self.ConnectDb()
        sql = """SELECT url, filename FROM downloadlist"""
        result = dataCon.ExecSQL(sql)
        urls = []
        for r in result:
            urls.append(Url(r[0], r[1]))
        dataCon.CloseConnection()
        return  urls
