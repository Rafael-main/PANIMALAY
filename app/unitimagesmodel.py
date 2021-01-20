from app import app,mysql
import random, string
import base64

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
		cur.execute("DELETE FROM unitimages WHERE imageID=%s",(imageID,))
		cur.execute("DELETE FROM images WHERE imageID=%s",(imageID,))
		mysql.connection.commit()

	@classmethod
	def selected(cls, unit_id):
		cur = mysql.connection.cursor()
		cur.execute("""SELECT images.filename,images.datum
			FROM units INNER JOIN unitimages ON units.unitID = unitimages.unitID
			INNER JOIN images
			ON unitimages.imageID = images.imageID
			WHERE units.unitID = %s""", (unit_id,))
		res = cur.fetchall()
		images = list()
		image_dct = dict()
		for result in res:
			image_dct['filename'] = result[0]
			blob = base64.b64encode(result[1])
			blob = blob.decode("UTF-8")
			image_dct['datum'] = blob
			images.append(image_dct)
			return images
