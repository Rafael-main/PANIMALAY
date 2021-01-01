from app import app,mysql
import random, string

class unitImages():
	def __init__(self,filename=None,datum=None):
		self.filename= filename
		self.datum = datum

	def addImage(self,unitid):
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
		cur.execute("INSERT INTO unitimages(unitID,imageID) VALUES (%s,%s)",(unitid,ID))
		mysql.connection.commit()

	def searchImages(self,unitid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM unitimages WHERE unitID=%s",(unitid,))
		imagesArray = cur.fetchall()
		imageIDs = []
		images = []
		for i in imagesArray:
			imageIDs.append(i[1])
		for j in imageIDs:
			cur.execute("SELECT * FROM images WHERE imageID=%s",(j,))
			image = cur.fetchone()
			images.append(image)
		return images

	def deleteImages(self,imageID):
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM unitimages WHERE imageID=%s",(imageID))
		cur.execute("DELETE FROM images WHERE imageID=%s",(imageID))
		mysql.connection.commit()
