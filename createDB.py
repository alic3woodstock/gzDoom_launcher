import functions
from dataFunctions import connect_db
from urlDB import insert_default_urls

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


class CreateDB:

    def create_game_table(self):
        data_con = connect_db()

        data_con.StartTransaction()
        data_con.ExecSQL("""CREATE TABLE IF NOT EXISTS groups(
                id integer PRIMARY KEY AUTOINCREMENT,
                groupname text);
            """)

        data_con.ExecSQL("""INSERT INTO groups(groupname) VALUES ('doom'),('heretic'),('hexen'),
                ('strife'),('other');
            """)

        sql = CREATE_TABS
        data_con.ExecSQL(sql)

        sql = """INSERT or IGNORE INTO tabs(tabindex, label, enabled)
            VALUES (?,?,?)"""
        params = [-1, "Mods", True]
        data_con.ExecSQL(sql, params)
        params = [0, "Games", True]
        data_con.ExecSQL(sql, params)
        params = [1, "Maps", True]
        data_con.ExecSQL(sql, params)

        data_con.ExecSQL(CREATE_GAMEDEF)

        data_con.ExecSQL("""CREATE TABLE IF NOT EXISTS files(
                id integer PRIMARY KEY AUTOINCREMENT,
                gameid integer,                        
                file text,
                FOREIGN KEY (gameid) REFERENCES gamedef(id) ON DELETE CASCADE);
            """)

        data_con.ExecSQL(CREATE_CONFIG)

        sql = """REPLACE INTO config (param, numvalue)
            VALUES ('dbversion', ?)"""
        params = [20000]
        data_con.ExecSQL(sql, params)

        data_con.ExecSQL(CREATE_DOWNLOADLIST)
        insert_default_urls(data_con)

        data_con.Commit()
        data_con.CloseConnection()

        self.WriteConfig("checkupdate", True, "bool")

    def UpdateDatabase(self):
        dataCon = connect_db()
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
            insert_default_urls()

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
        dataVersion = self.ReadConfig('gzdversion', 'text')
        dataHash = self.ReadConfig('gzdhash', 'text')
        if dataVersion == version and dataHash == filehash:
            return True
        else:
            return False

    def CheckDbVersion(self):
        dataCon = connect_db()
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
            version = 0
            sql = """SELECT numvalue FROM config WHERE param = 'dbversion'"""
            versionData = dataCon.ExecSQL(sql)
            for v in versionData:
                version = v[0]

            return int(version)

    def ReadConfig(self, param="", valuetype="text"):
        dataCon = connect_db()
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
        return returnValue

    def WriteConfig(self, param="", value=None, value_type="text"):
        dataCon = connect_db()
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
        dataCon.StartTransaction()
        dataCon.ExecSQL(sql, params)
        dataCon.Commit()
        dataCon.CloseConnection()
