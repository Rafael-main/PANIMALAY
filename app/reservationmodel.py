from app import app,mysql
from datetime import datetime

class newReservation():
	def __init__(self,username=None,unitID=None,reservationDate=None):
		self.username = username
		self.unitID = unitID
		self.reservationDate = reservationDate

	def addReservation(self):
		status = 'WFOR'
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO reservations(username,unitID,reservationDate,status) VALUES (%s,%s,%s,%s)",(self.username,self.unitID,self.reservationDate,status))
		mysql.connection.commit()

	@classmethod
	def accept(cls,rNo):
		status = 'A'
		cur = mysql.connection.cursor()
		cur.execute("UPDATE reservations SET status=%s WHERE reservationNo=%s",(status,rNo))
		mysql.connection.commit()

	@classmethod
	def decline(cls,rNo):
		status = 'D'
		cur = mysql.connection.cursor()
		cur.execute("UPDATE reservations SET status=%s WHERE reservationNo=%s",(status,rNo))
		mysql.connection.commit()

	@classmethod
	def confirm(cls,rNo,username,unitID):
		status = 'C'
		checkinDate =datetime.today().strftime('%Y-%m-%d')
		cur = mysql.connection.cursor()
		cur.execute("UPDATE reservations SET status=%s WHERE reservationNo=%s",(status,rNo))
		cur.execute("INSERT INTO renters(username,unitID,checkinDate) VALUES (%s,%s,%s)",(username,unitID,checkinDate))
		mysql.connection.commit()
	
	@classmethod
	def deleteReservation(cls,rNo):
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM reservations WHERE reservationNo=%s",(rNo,))
		mysql.connection.commit()


	@classmethod
	def searchReservations(cls):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM reservations")
		reservations = cur.fetchall()
		return reservations

