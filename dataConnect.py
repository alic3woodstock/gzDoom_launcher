import sqlite3
from sqlite3 import Error

class SqliteDB():
	_connection = None
	
	def __init__(self, dbName):
		self.CreateConnection(dbName)
	
	def CreateConnection(self, dbName):
		try:
			self._connection = sqlite3.connect(dbName)
			return True
		except Error as e:
			print(e)	
			return False	
			
	def GetConnection(self):
		return self._connection
	
	def CloseConnection(self):
		if self._connection:
			self._connection.close()
			
	def ExecSQL(self, sql, params = ""):
		try:
			return self._connection.execute(sql, params)
		except Error as e:
			print(e)
			return ""
		
	def StartTransaction(self):
		self._connection.execute("""BEGIN TRANSACTION;""")
	
	def Commit(self):
		self._connection.execute("""COMMIT;""")
		