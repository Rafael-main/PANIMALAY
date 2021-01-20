from app import app,mysql

class account():
	def __init__(self,username=None,email=None,password=None,accountType=None):
		self.username = username
		self.email = email
		self.password = password
		self.accountType = accountType

	def usernameValidate(self,username):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts WHERE username=%s",(username,))
		result = cur.fetchone()
		if bool(result)==True:
			return True
		else:
			return False
	@classmethod
	def searchForLogin(cls,username,password):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts WHERE username=%s",(username,))
		result = cur.fetchone()
		if result is not None and len(result)!=0:
			if password==result[2]:
				return True
			else:
				return "Invalid password!"
		else:
			return "Invalid username!"
			
	def addAccount(self):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts")
		accounts = cur.fetchall()

		#check if the username is not taken
		invalidUsernameFlag = 0
		for account in accounts:
			if self.username==account[0]:
				invalidUsernameFlag+=1

		if invalidUsernameFlag!=0:
			print("Invalid Username")
		else:
			cur.execute("INSERT INTO accounts(username,email,password,accountType) VALUES (%s,%s,%s,%s)", (self.username,self.email,self.password,self.accountType))
			mysql.connection.commit()
	
	@classmethod
	def usernames(cls):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts")
		accounts = cur.fetchall()
		usernames = []
		for account in accounts:
			usernames.append(account[0])
		return usernames


	@classmethod
	def profileData(cls,username):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts WHERE username=%s",(username,))
		acccountData = cur.fetchone()
		cur.execute("SELECT * FROM profiles WHERE username=%s",(username,))
		profileData = cur.fetchone()
		data = [acccountData,profileData]
		return data
		
	def updateAccount(self):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE accounts SET email=%s,password=%s WHERE username=%s",(self.email,self.password,self.username))
		mysql.connection.commit()

	@classmethod
	def accountData(cls,username):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts WHERE username=%s",(username,))
		acccountData = cur.fetchone()
		return acccountData

	@classmethod
	def changeEmail(cls,username,newEmail):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE accounts SET email=%s WHERE username=%s",(newEmail,username))
		mysql.connection.commit()

	@classmethod
	def changePassword(cls,username,newPassword):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE accounts SET password=%s WHERE username=%s",(newPassword,username))
		mysql.connection.commit()

