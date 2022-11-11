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
        dataCon.ExecSQL("""CREATE TABLE IF NOT EXISTS files(
            id integer PRIMARY KEY AUTOINCREMENT,
            gameid integer,                        
            file text,
            FOREIGN KEY (gameid) REFERENCES gamedef(id) ON DELETE CASCADE);
        """)           
                
        dataCon.ExecSQL("""CREATE TABLE IF NOT EXISTS gamedef(
                id integer PRIMARY KEY AUTOINCREMENT,
                name text,
                tabindex integer NOT NULL,
                gamexec text,
                modgroup text,
                lastrunmod integer NOT NULL,
                iwad text);                                
            """)
        dataCon.CloseConnection()
        
    def CleanGameTable(self):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        dataCon.ExecSQL("""DROP TABLE files;""")        
        dataCon.ExecSQL("""DROP TABLE gamedef;""")        
        dataCon.Commit()
        dataCon.CloseConnection()
        self.CreateGameTable()        
        
    def InsertGame(self, game):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()
        sql = """INSERT INTO gamedef(name,tabindex,gamexec,modgroup,lastrunmod,iwad)
            VALUES (?,?,?,?,?,?);"""
        
        params = (game.GetItem().GetText(), game.GetTab(), game.GetExec(), game.GetGroup(),
                  game.GetLastMod(),game.GetIWad())
        
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
        gameData = dataCon.ExecSQL("""SELECT id, name, tabindex, gamexec, modgroup, lastrunmod, iwad
         FROM gamedef ORDER BY tabindex,name""")
        for game in gameData:
            g = gameDef.GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6])            
            g.SetFiles([])
            fileData = dataCon.ExecSQL("""SELECT file FROM files WHERE gameid = ?""",[game[0]])
            for f in fileData:
                g.GetFiles().append(f[0])
            games.append(g)
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
        
    def SelectGameById(self, gameId):
        dataCon = self.ConnectDb()
        gameData = dataCon.ExecSQL("""SELECT id, name, tabindex, gamexec, modgroup, lastrunmod, iwad
         FROM gamedef WHERE id=? ORDER BY id""", [gameId])
        game = gameData.fetchone()
        g = gameDef.GameDef(game[0], game[1], game[2], game[3], game[4], game[5], game[6])            
        g.SetFiles([])
        fileData = dataCon.ExecSQL("""SELECT file FROM files WHERE gameid = ?""",[game[0]])
        for f in fileData:
            g.GetFiles().append(f[0])
        return(g)
    
    def UpdateGame(self, game, updateFiles = False):
        dataCon = self.ConnectDb()
        dataCon.StartTransaction()

        sql = """UPDATE gamedef SET name=?, tabindex=?, gamexec=?, modgroup=?, iwad=? WHERE id=?"""
        params = [game.GetItem().GetText(), game.GetTab(), game.GetExec(), game.GetGroup(), game.GetIWad(),
                  game.GetItem().GetData()]        
        dataCon.ExecSQL(sql, params)
        
        if updateFiles:
            sql = """DELETE FROM files WHERE gameid=?"""
            params = [game.GetItem().GetData()]
            dataCon.ExecSQL(sql, params)        
            sql = """INSERT INTO files(gameid,file) values(?,?)"""
            for f in game.GetFiles():
                params = ([game.GetItem().GetData(), f]) 
                dataCon.ExecSQL(sql,params)             
                
        dataCon.Commit()

        
