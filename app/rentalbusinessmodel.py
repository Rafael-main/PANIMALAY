from app import app,mysql
import random, string

class rentalBusiness():
	def __init__(self,username=None,rbName=None,email=None,phoneNumber=None,description=None):
		self.username = username
		self.rbName = rbName
		self.email = email
		self.phoneNumber = phoneNumber
		self.description = description

	def addRentalBusiness(self):
		cur = mysql.connection.cursor()
		flag = 0 
		while flag==0:
			randomstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
			prefix= 'RENTAL'
			rbid = prefix+randomstr
			cur.execute("SELECT * FROM rentalbusiness WHERE RBID=%s",(rbid,))
			rb = cur.fetchall()
			if len(rb)!=0:
				flag = 0 
			else:
				flag = 1
		if flag == 1:
			cur.execute("INSERT INTO rentalbusiness(ownersUserName,rbName,RBID,description,email) VALUES (%s,%s,%s,%s,%s)",(self.username,self.rbName,rbid,self.description,self.email))
			cur.execute("INSERT INTO rentalbusinessphonenumber(RBID,phoneNumber) VALUES (%s,%s)",(rbid,self.phoneNumber))
			mysql.connection.commit()

	@classmethod		
	def searchRentalBusiness(cls,username):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM rentalbusiness WHERE ownersUserName=%s",(username,))
		rb = cur.fetchone()
		if rb!=None:
			return rb
		else:
			return None
	@classmethod
	def searchRentalBusinessPhoneNumber(cls,RBID):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM rentalbusinessphonenumber WHERE RBID=%s",(RBID,))
		phoneNumber = cur.fetchone()
		phoneNumber = phoneNumber[1]
		return phoneNumber

	
	def updateRentalBusiness(self,rbid):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE rentalbusiness SET rbName=%s,description=%s,email=%s WHERE RBID=%s",(self.rbName,self.description,self.email,rbid))
		cur.execute("UPDATE rentalbusinessphonenumber  SET phoneNumber=%s WHERE RBID=%s",(self.phoneNumber,rbid))
		mysql.connection.commit()