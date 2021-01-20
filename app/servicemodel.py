from app import app,mysql
class newServices():
	def __init__(self,service=None,RBID=None):
		self.service = service
		self.RBID = RBID

	def addService(self):
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO services(RBID,service) VALUES (%s,%s)",(self.RBID,self.service))
		mysql.connection.commit()

	@classmethod
	def searchServices(cls,rbid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM services WHERE RBID=%s",(rbid,))
		services = cur.fetchall()
		if services!=None:
			return services
		else:
			services = None
			return services

	@classmethod
	def updateSrvc(cls,srvc,serviceno):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE services SET service=%s WHERE serviceNo=%s",(srvc,serviceno))
		mysql.connection.commit()

	@classmethod
	def deleteSrvc(cls,serviceno):
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM services WHERE serviceNo=%s",(serviceno,))
		mysql.connection.commit()
