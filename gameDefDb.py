import dataConnect
import gameDef

class GameDefDb():
    _dataCon = None
    
    def GetDataCon(self):
        return self._dataCon
    
    def ConnectDb(self):
        self._dataCon = dataConnect.SqliteDB('games.sqlite3')
        return self._dataCon
        
    def CreateGameTable(self):
        dataCon = self.ConnectDb()
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
                gamexec text,
                modgroup text,
                lastrunmod integer NOT NULL,
                iwad text);                                
            """)
        dataCon.closeConnection()
        
    def CleanGameTable(self):
        dataCon = self.ConnectDb()
        dataCon.startTransaction()
        dataCon.execSQL("""DROP TABLE files;""")        
        dataCon.execSQL("""DROP TABLE gamedef;""")        
        dataCon.commit()
        dataCon.closeConnection()
        self.CreateGameTable()        
        
    def InsertGame(self, game):
        dataCon = self.ConnectDb()
        dataCon.startTransaction()
        sql = """INSERT INTO gamedef(name,tabindex,gamexec,modgroup,lastrunmod,iwad)
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
        
    def SelectAllGames(self):
        games = []
        
        dataCon = self.ConnectDb()
        gameData = dataCon.execSQL("""SELECT id, name, tabindex, gamexec, modgroup, lastrunmod, iwad
         FROM gamedef ORDER BY id""")
        for game in gameData:
            g = gameDef.GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6])            
            g.SetFiles([])
            fileData = dataCon.execSQL("""SELECT file FROM files WHERE gameid = ?""",[game[0]])
            for f in fileData:
                g.GetFiles().append(f[0])
            games.append(g)
        return games               

    def UpdateLastRunMod(self, game, mod):
        dataCon = self.ConnectDb()
        dataCon.startTransaction()
        dataCon.execSQL("""UPDATE gamedef SET lastrunmod=? WHERE id=?""", [mod.GetItem().GetData(),
                                                                           game.GetItem().GetData()])
        dataCon.commit()