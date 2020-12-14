from app import app,mysql

class account():
	def __init__(self,username=None,email=None,password=None,accountType=None):
		self.username = username
		self.email = email
		self.password = password
		self.accountType = accountType

	def search(self,usrnm):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts WHERE username=%s",(usrnm,))
		result = cur.fetchall()
		if len(result)>0:
			return True
		else:
			return False
	@classmethod
	def searchForLogin(cls,emailOrUsername,password):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM accounts WHERE username=%s",(emailOrUsername,))
		result = cur.fetchone()
		if result is not None and len(result)!=0:
			if password==result[2]:
				return True
			else:
				return "Invalid password!"
		else:
			return "Invalid email or password!"
			
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
