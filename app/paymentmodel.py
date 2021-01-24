from app import app,mysql

class newPayment():
	def __init__(self,payersUsername=None,amount=None,paymentDate=None,unitRented=None):
		self.payersUsername = payersUsername
		self.amount = amount
		self.paymentDate = paymentDate
		self.unitRented = unitRented

	def addPayment(self,rbid):
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO payments(username,RBID,amount,paymentDate,unitRented) VALUES (%s,%s,%s,%s,%s)",(self.payersUsername,rbid,self.amount,self.paymentDate,self.unitRented))
		mysql.connection.commit()

	def updatePayment(self,paymentNumber):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE payments SET username=%s,amount=%s,paymentDate=%s,unitRented=%s WHERE paymentNo=%s",(self.payersUsername,self.amount,self.paymentDate,self.unitRented,paymentNumber))
		mysql.connection.commit()

	def searchPayments(self,rbid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM payments WHERE RBID=%s",(rbid,))
		paymentRecord = cur.fetchall()
		if paymentRecord!=None:
			return paymentRecord
		else:
			return None

	def deletePayment(self,paymentNumber):
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM payments WHERE paymentNo=%s",(paymentNumber,))
		mysql.connection.commit()

	@classmethod
	def searchPaymentsForRenter(cls,username):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM payments WHERE username=%s",(username,))
		paymentRecord = cur.fetchall()
		if paymentRecord!=None:
			return paymentRecord
		else:
			return None

	@classmethod
	def searchUnitForPayment(cls):
		cur = mysql.connection.cursor()
		cur.execute("""SELECT * FROM (SELECT units.unitID,units.RBID,units.capacity,units.rate,units.unitType,units.genderAccommodation,rentalbusiness.rbName
					FROM units
					INNER JOIN rentalbusiness ON rentalbusiness.RBID = units.RBID) AS unitInfo""")
		data = cur.fetchall()
		
		return data
