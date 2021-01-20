from app import app,mysql
import random, string



class profilePicture():
	def __init__(self,filename=None,datum=None):
		self.filename = filename
		self.datum = datum

	
	def addProfilePicture(self,profileID):
		cur = mysql.connection.cursor()
		flag = 0
		if flag==0:
			randomstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(11))
			prefix= 'IMAGE'
			ID = prefix+randomstr
			cur.execute("SELECT * FROM images WHERE imageID=%s",(ID,))
			duplicateChecker = cur.fetchone()
			if duplicateChecker!=None:
				flag = flag
			else:
				flag = 1
		cur.execute("INSERT INTO images(imageID,filename,datum) VALUES (%s,%s,%s)",(ID,self.filename,self.datum))
		cur.execute("INSERT INTO profilepictures(profileID,imageID) VALUES (%s,%s)",(profileID,ID))
		mysql.connection.commit()

	def updateProfilePicture(self,profileID):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM profilepictures WHERE profileID=%s",(profileID,))
		ID = cur.fetchone()
		ID = ID[1]
		cur.execute("""UPDATE images SET filename=%s, datum=%s WHERE imageID=%s""",(self.filename,self.datum,ID))
		mysql.connection.commit()

		
	@classmethod
	def retrieveFile(cls,ID):
		cur = mysql.connection.cursor(buffered=True)
		cur.execute("SELECT * FROM profilepictures WHERE profileID=%s",(ID,))
		profileImageID = cur.fetchone()
		if profileImageID!=None:
			profileImageID = profileImageID[1]
			cur.execute("SELECT * FROM images WHERE imageID=%s",(profileImageID,))
			datum = cur.fetchone()
			return datum
		else:
			return None

	@classmethod
	def searchAllProfilePictures(cls):
		cur = mysql.connection.cursor()
		cur.execute("""SELECT profilepictures.profileID,images.imageID,images.filename,images.datum FROM profilepictures
				INNER JOIN images ON profilepictures.imageID = images.imageID""")
		profilePictures = cur.fetchall()
		return profilePictures
