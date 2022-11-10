import sqlite3
from sqlite3 import Error

class SqliteDB():
	_connection = None
	
	def __init__(self, dbName):
		self.createConnection(dbName)
	
	def createConnection(self, dbName):
		try:
			self._connection = sqlite3.connect(dbName)
			return True
		except Error as e:
			print(e)	
			return False	
			
	def getConnection(self):
		return self._connection
	
	def closeConnection(self):
		if self._connection:
			self._connection.close()
			
	def execSQL(self, sql, params = ""):
		try:
			return self._connection.execute(sql, params)
		except Error as e:
			print(e)
			return ""
		
	def startTransaction(self):
		self._connection.execute("""BEGIN TRANSACTION;""")
	
	def commit(self):
		self._connection.execute("""COMMIT;""")
		