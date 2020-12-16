from app import app,mysql


class Add_Units(object):
	def __init__(self, typee=None, rate = None, capacity = None, gender_accomodation = None, description = None):
		self.typee = typee
		self.rate = rate
		self.capacity = capacity
		self.gender_accomodation = gender_accomodation
		self.description = description

	def addUnit(self):
		cur.mysql.connection.cursor()
		cur.execute("INSERT INTO addunit(typee, rate, capacity, gender_accomodation, description) VALUES(%s,%s,%s,%s,%s)",(self.typee, self.rate,self.capacity, self.gender_accomodation, self.description))
		mysql.connection.commit()
