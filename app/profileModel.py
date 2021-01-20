from app import app, mysql
import random, string

class profile():
	def __init__(self,username=None,firstName=None,lastName=None,birthDate=None,gender=None):
		self.username = username
		self.firstName = firstName
		self.lastName = lastName
		self.birthDate = birthDate
		self.gender = gender


	def addProfile(self,accountType,phoneNumber):
		cur = mysql.connection.cursor()
		flag = 0
		while flag==0:
			if accountType=="Renter":
				randomstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
				prefix= 'RENTER'
				profileID = prefix+randomstr
			else:
				randomstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(11))
				prefix= 'OWNER'
				profileID = prefix+randomstr

			cur.execute("SELECT * FROM profiles WHERE profileID=%s",(profileID,))
			result = cur.fetchall()
			if len(result)!=0:
				flag=0
			else:
				flag=1
		if flag==1:
			cur.execute("INSERT INTO profiles(username,profileID,firstName,lastName,birthDate,sex) VALUES (%s,%s,%s,%s,%s,%s)",(self.username,profileID,self.firstName,self.lastName,self.birthDate,self.gender))
			cur.execute("INSERT INTO profilephonenumber(profileID,phoneNumber) VALUES (%s,%s)",(profileID,phoneNumber))
			mysql.connection.commit()

	def updateProfile(self,profileID):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE profiles SET firstName=%s,lastName=%s,birthDate=%s,sex=%s WHERE profileID=%s",(self.firstName,self.lastName,self.birthDate,self.gender,profileID))
		mysql.connection.commit()


	def allProfiles(self):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM profiles")
		profiles = cur.fetchall()
		return profiles

	@classmethod
	def searchPhoneNumber(cls,username):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM profiles WHERE username=%s",(username,))
		profile = cur.fetchone()
		if profile!=None:
			pID = profile[1]
			cur.execute("SELECT * FROM profilephonenumber WHERE profileID=%s",(pID,))
			phoneNumber = cur.fetchall()
			return phoneNumber
	@classmethod
	def validatePhoneNumber(cls,phoneNumber):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM profilephonenumber WHERE phoneNumber=%s",(phoneNumber,))
		phoneNumber = cur.fetchall()
		if bool(phoneNumber)==True:
			return True
		else:
			return False
	@classmethod
	def updatePhoneNumber(cls,phoneNumber,profileID):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE profilephonenumber SET phoneNumber=%s WHERE profileID=%s",(phoneNumber,profileID))
		mysql.connection.commit()

	def allPhoneNumbers(self):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM profilephonenumber")
		phoneNumbers = cur.fetchall()
		listOfPhoneNumbers = []
		for p in phoneNumbers:
			listOfPhoneNumbers.append(p[1])
		return listOfPhoneNumbers

	def allPhoneNumberWithID(self):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM profilephonenumber")
		phoneNumbers = cur.fetchall()
		return phoneNumbers
	@classmethod
	def searchProfile(cls,usrnm):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM profiles WHERE username=%s",(usrnm,))
		profile = cur.fetchall()
		return profile
