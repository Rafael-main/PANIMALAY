from app import app,mysql
class newProtocols():
	def __init__(self,protocols=None,RBID=None):
		self.protocols = protocols
		self.RBID = RBID

	def addProtocols(self):
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO protocols(RBID,protocol) VALUES (%s,%s)",(self.RBID,self.protocols))
		mysql.connection.commit()

	@classmethod
	def searchProtocol(cls,rbid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM protocols WHERE RBID=%s",(rbid,))
		protocol = cur.fetchone()
		if protocol!=None:
			protocol = protocol[1]
		else:
			protocol = None
		return protocol

	def updateProtocols(self):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE protocols SET protocol=%s WHERE RBID=%s",(self.protocols,self.RBID))
		mysql.connection.commit()