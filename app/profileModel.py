from app import app, mysql
import random, string

class profile():
	def __init__(self,username=None,firstName=None,lastName=None,birthDate=None,gender=None):
		self.username = username
		self.firstName = firstName
		self.lastName = lastName
		self.birthDate = birthDate
		self.gender = gender

	def addProfile(self):
		cur = mysql.connection.cursor()
		flag = 0
		while flag==0:
			randomstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
			prefix= 'RENTER'
			profileID = prefix+randomstr
			cur.execute("SELECT * FROM profiles WHERE profileID=%s",(profileID,))
			result = cur.fetchall()
			if len(result)!=0:
				flag=0
			else:
				flag=1
		if flag==1:
			cur.execute("INSERT INTO profiles(username,profileID,firstName,lastName,birthDate,sex) VALUES (%s,%s,%s,%s,%s,%s)",(self.username,profileID,self.firstName,self.lastName,self.birthDate,self.gender))
			mysql.connection.commit()
		