from app import app,mysql
class newProtocol():
	def __init__(self,protocol=None,RBID=None):
		self.protocol = protocol
		self.RBID = RBID

	def addProtocol(self):
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO protocols(RBID,protocol) VALUES (%s,%s)",(self.RBID,self.protocol))
		mysql.connection.commit()

	@classmethod
	def searchProtocols(cls,rbid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM protocols WHERE RBID=%s",(rbid,))
		protocols = cur.fetchall()
		if protocols!=None:
			return protocols
		else:
			protocols = None
			return protocols

	@classmethod
	def updatePrtcl(cls,prtcl,protocolno):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE protocols SET protocol=%s WHERE protocolNo=%s",(prtcl,protocolno))
		mysql.connection.commit()

	@classmethod
	def deletePrtcl(cls,protocolno):
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM protocols WHERE protocolNo=%s",(protocolno,))
		mysql.connection.commit()