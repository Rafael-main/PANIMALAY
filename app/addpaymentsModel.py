from app import app,mysql


class Add_Payments(object):
	def __init__(self,,firstName=None,lastName=None, transaction = None, date=None):
		self.firstName = firstName
		self.lastName = lastName
		self.transaction = transaction
		self.date = date

	def addpayments(self):
		cur.mysql.connection.cursor()
		cur.execute("INSERT INTO addpayments(firstName, lastName, transaction, date) VALUES(%s,%s,%s,%s)",(self.firstName, self.lastName,self.transaction, self.date,))
		mysql.connection.commit()
