from app import app,mysql
class newServices():
	def __init__(self,services=None,RBID=None):
		self.services = services
		self.RBID = RBID

	def addServices(self):
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO services(RBID,service) VALUES (%s,%s)",(self.RBID,self.services))
		mysql.connection.commit()

	@classmethod
	def searchServices(cls,rbid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM services WHERE RBID=%s",(rbid,))
		service = cur.fetchone()
		if service!=None:
			service = service[1]
		else:
			service = None
		return service

	def updateServices(self):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE services SET service=%s WHERE RBID=%s",(self.services,self.RBID))
		mysql.connection.commit()