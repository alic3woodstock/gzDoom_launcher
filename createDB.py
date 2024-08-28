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
                filename text UNIQUE ,
                sha_hash text UNIQUE)
            """


def check_db_version():
    data_con = connect_db()
    sql = """SELECT sql FROM sqlite_master WHERE tbl_name = ?"""
    params = ["config"]
    text = data_con.exec_sql(sql, params)
    str_table = ""
    for t in text:
        if t[0]:
            str_table = t[0]
    if str_table.lower().find("config") < 0:
        return 0
    else:
        version = 0
        sql = """SELECT numvalue FROM config WHERE param = 'dbversion'"""
        version_data = data_con.exec_sql(sql)
        for v in version_data:
            version = v[0]

        return int(version)


def update_database():
    data_con = connect_db()
    db_version = check_db_version()

    data_con.start_transaction()
    sql = """SELECT sql FROM sqlite_master WHERE tbl_name = ?"""
    params = ["config"]
    text = data_con.exec_sql(sql, params)
    str_table = ""
    for t in text:
        if t[0]:
            str_table = t[0]

    if str_table.lower().find("config") < 0:
        sql = """SELECT sql FROM sqlite_master WHERE tbl_name = ?"""
        params = ["gamedef"]
        text = data_con.exec_sql(sql, params)
        for t in text:
            sql = t[0]

        if sql.lower().find("cmdparams") < 0:
            sql2 = """ALTER TABLE gamedef ADD COLUMN cmdparams text NOT NULL DEFAULT ''"""
            data_con.exec_sql(sql2)

        if sql.lower().find("ismod") < 0:
            sql2 = """ALTER TABLE gamedef ADD COLUMN ismod BOOLEAN NOT NULL DEFAULT false"""
            data_con.exec_sql(sql2)
            sql2 = """UPDATE gamedef SET ismod = true WHERE tabindex = 2"""
            data_con.exec_sql(sql2)
            sql2 = """UPDATE gamedef SET tabindex = -1 WHERE ismod = true"""
            data_con.exec_sql(sql2)
            sql2 = """ALTER TABLE gamedef DROP COLUMN ismod"""
            data_con.exec_sql(sql2)

        sql = """CREATE TABLE IF NOT EXISTS gzdoom_version(
            id INTEGER PRIMARY KEY,
            version text,
            sha256 text)"""
        data_con.exec_sql(sql)

        data_con.exec_sql(CREATE_CONFIG)

    if db_version < 10100:
        data_con.exec_sql(CREATE_TABS)

        sql = """REPLACE INTO tabs(tabindex, label, enabled)
            VALUES (?,?,?)"""
        params = [-1, "Mods", True]
        data_con.exec_sql(sql, params)
        params = [0, "Games", True]
        data_con.exec_sql(sql, params)
        params = [1, "Maps", True]
        data_con.exec_sql(sql, params)

        sql = """UPDATE gamedef SET tabindex=0 WHERE id IN (
            SELECT DISTINCT g.id FROM gamedef g LEFT JOIN tabs t on t.tabindex = g.tabindex WHERE 
            t.tabindex IS NULL)"""
        data_con.exec_sql(sql)

        data_con.exec_sql("""ALTER TABLE gamedef RENAME TO gamedef_old""")
        data_con.exec_sql(CREATE_GAMEDEF)
        data_con.exec_sql("""INSERT INTO gamedef SELECT * FROM gamedef_old""")
        data_con.exec_sql("""DROP TABLE gamedef_old""")

    if db_version < 20001:
        data_con.exec_sql("""DROP TABLE IF EXISTS downloadlist""")
        data_con.exec_sql(CREATE_DOWNLOADLIST)
        insert_default_urls()

    sql = """REPLACE INTO config (param, numvalue)
        VALUES (?, ?)"""
    params = ['dbversion', functions.version_number()]
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


def check_gz_doom_version(version, filehash):
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


def create_game_table():
    data_con = connect_db()

    data_con.start_transaction()
    data_con.exec_sql("""CREATE TABLE IF NOT EXISTS groups(
            id integer PRIMARY KEY AUTOINCREMENT,
            groupname text);
        """)

    data_con.exec_sql("""INSERT INTO groups(groupname) VALUES ('doom'),('heretic'),('hexen'),
            ('strife'),('other');
        """)

    sql = CREATE_TABS
    data_con.exec_sql(sql)

    sql = """INSERT or IGNORE INTO tabs(tabindex, label, enabled)
        VALUES (?,?,?)"""
    params = [-1, "Mods", True]
    data_con.exec_sql(sql, params)
    params = [0, "Games", True]
    data_con.exec_sql(sql, params)
    params = [1, "Maps", True]
    data_con.exec_sql(sql, params)

    data_con.exec_sql(CREATE_GAMEDEF)

    data_con.exec_sql("""CREATE TABLE IF NOT EXISTS files(
            id integer PRIMARY KEY AUTOINCREMENT,
            gameid integer,                        
            file text,
            FOREIGN KEY (gameid) REFERENCES gamedef(id) ON DELETE CASCADE);
        """)

    data_con.exec_sql(CREATE_CONFIG)

    sql = """REPLACE INTO config (param, numvalue)
        VALUES ('dbversion', ?)"""
    params = [20001]
    data_con.exec_sql(sql, params)

    data_con.exec_sql(CREATE_DOWNLOADLIST)
    insert_default_urls(data_con)

    data_con.commit()
    data_con.close_connection()

    write_config("checkupdate", True, "bool")


def update_gzdoom_version(version, filehash):
    write_config('gzdversion', version, 'text')
    write_config('gzdhash', filehash, 'text')


class CreateDB:
    pass
