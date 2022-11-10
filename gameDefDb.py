import dataConnect
import gameDef
from numpy.testing._private.parameterized import param

class GameDefDb():
    _dataCon = None
    
    def getDataCon(self):
        return self._dataCon
    
    def connectDb(self):
        self._dataCon = dataConnect.SqliteDB('games.sqlite3')
        return self._dataCon
        
    def createGameTable(self):
        dataCon = self.connectDb()
        dataCon.execSQL("""CREATE TABLE IF NOT EXISTS files(
            id integer PRIMARY KEY AUTOINCREMENT,
            gameid integer,                        
            file text,
            FOREIGN KEY (gameid) REFERENCES gamedef(id) ON DELETE CASCADE);
        """)           
                
        dataCon.execSQL("""CREATE TABLE IF NOT EXISTS gamedef(
                id integer PRIMARY KEY AUTOINCREMENT,
                name text,
                tabindex integer NOT NULL,
                gameexec text,
                modgroup text,
                lastrunmod integer NOT NULL,
                iwad text);                                
            """)
        dataCon.closeConnection()
        
    def cleanGameTable(self):
        dataCon = self.connectDb()
        dataCon.startTransaction()
        dataCon.execSQL("""DROP TABLE files;""")        
        dataCon.execSQL("""DROP TABLE gamedef;""")        
        dataCon.commit()
        dataCon.closeConnection()
        self.createGameTable()        
        
    def insertGame(self, game):
        dataCon = self.connectDb()
        dataCon.startTransaction()
        sql = """INSERT INTO gamedef(name,tabindex,gameexec,modgroup,lastrunmod,iwad)
            VALUES (?,?,?,?,?,?);"""
        
        params = (game.GetItem().GetText(), game.GetTab(), game.GetExec(), game.GetGroup(),
                  game.GetLastMod(),game.GetIWad())
        
        dataCon.execSQL(sql, params)
        
        gameIds = dataCon.execSQL("""SELECT id FROM gamedef ORDER BY id DESC LIMIT 1;""")                
        gameId = gameIds.fetchall()[0][0]
        
        sql = """INSERT INTO files(gameid,file) VALUES(?,?)"""
        for f in game.GetFiles():
            params = (gameId, f)
            dataCon.execSQL(sql, params)        
                
        dataCon.commit()
        dataCon.closeConnection()
    
        
