from app import app,mysql
import random, string


class newUnit():
	def __init__(self,username=None,unitType=None,genderAccommodation=None,capacity=None,rate=None,street=None,barangay=None,cityOrMunicipality=None,province=None,latitude=None,longitude=None,facilities=None):
		self.username = username
		self.unitType = unitType
		self.genderAccommodation = genderAccommodation
		self.capacity = capacity
		self.rate = rate
		self.street = street
		self.barangay = barangay
		self.cityOrMunicipality = cityOrMunicipality 
		self.province = province
		self.latitude = latitude
		self.longitude = longitude
		self.facilities = facilities

	
	def addUnit(self):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM rentalbusiness WHERE ownersUserName=%s",(self.username,))
		RBID = cur.fetchone()
		RBID = RBID[2]
		flag = 0
		while flag==0:
			randomstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
			prefix= 'UNIT'
			unitID = prefix+randomstr

			cur.execute("SELECT * FROM units WHERE unitID=%s",(unitID,))
			validateUnitID = cur.fetchone()
			if validateUnitID!=None:
				flag = 0
			else:
				flag = 1
		if flag == 1:
			cur.execute("INSERT INTO units(RBID,unitID,capacity,rate,unitType,genderAccommodation) VALUES (%s,%s,%s,%s,%s,%s)",(RBID,unitID,self.capacity,self.rate,self.unitType,self.genderAccommodation))


		flag = 0
		while flag==0:
			randomstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
			prefix= 'LOCATION'
			locationID = prefix+randomstr

			cur.execute("SELECT * FROM units WHERE unitID=%s",(locationID,))
			validatelocationID = cur.fetchone()
			if validatelocationID!=None:
				flag = 0
			else:
				flag = 1
		if flag == 1:
			cur.execute("INSERT INTO locations(unitID,locationID,latitude,longitude,street,barangay,cityOrMunicipality,province) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(unitID,locationID,self.latitude,self.longitude,self.street,self.barangay,self.cityOrMunicipality,self.province))
		cur.execute("INSERT INTO facilities(unitID,facility) VALUES (%s,%s)",(unitID,self.facilities))
		mysql.connection.commit()


	@classmethod
	def searchUnit(cls,rbid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM units WHERE RBID=%s",(rbid,))
		ownedUnits = cur.fetchall()
		return ownedUnits

	def updateUnit(self,unitid):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE units SET capacity=%s,rate=%s,unitType=%s,genderAccommodation=%s WHERE unitID=%s",(self.capacity,self.rate,self.unitType,self.genderAccommodation,unitid))
		cur.execute("UPDATE locations SET latitude=%s,longitude=%s,street=%s,barangay=%s,cityOrMunicipality=%s,province=%s WHERE unitID=%s",(self.latitude,self.longitude,self.street,self.barangay,self.cityOrMunicipality,self.province,unitid))

		cur.execute("SELECT * FROM facilities WHERE unitID=%s",(unitid,))
		checker = cur.fetchall()
		if len(checker)==0:
			cur.execute("INSERT INTO facilities(unitID,facility) VALUES (%s,%s)",(unitID,self.facilities))
		else:
			cur.execute("UPDATE facilities(unitID,facility) VALUES (%s,%s)",(unitID,self.facilities))
		mysql.connection.commit()

	@classmethod
	def searchForUpdateUnit(cls,unitid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM units WHERE unitID=%s",(unitid,))
		unitToUpdate = cur.fetchone()
		return unitToUpdate

	@classmethod
	def searchForUpdateUnitLocation(cls,unitid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM locations WHERE unitID=%s",(unitid,))
		unitToUpdateLocation = cur.fetchone()
		return unitToUpdateLocation

	@classmethod
	def searchForUpdateUnitFacilities(cls,unitid):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM facilities WHERE unitID=%s",(unitid,))
		unitToUpdateFacilities = cur.fetchone()
		return unitToUpdateFacilities

	@classmethod
	def delUnit(cls,unitid):
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM units WHERE unitID=%s",(unitid,))
		mysql.connection.commit()

	@classmethod
	def searchResult(cls,location,unittype,genderAcco,cap):
		cur = mysql.connection.cursor()
		cur.execute("SET @locationInput=%s",(location,))
		cur.execute("SET @unittypeInput=%s",(unittype,))
		cur.execute("SET @genderAccoInput=%s",(genderAcco,))
		cur.execute("SET @capInput=%s",(cap,))
		cur.execute("""SELECT * FROM (SELECT units.unitID,units.RBID,units.capacity,units.rate,units.unitType,units.genderAccommodation,locations.locationID,locations.latitude,locations.longitude,locations.street,locations.barangay,locations.cityOrMunicipality,locations.province
		FROM units
		INNER JOIN locations
		ON units.unitID=locations.unitID) AS unitsInfo
		WHERE (street LIKE CONCAT('%',@locationInput,'%') or barangay LIKE CONCAT('%',@locationInput,'%') or cityOrMunicipality LIKE CONCAT('%',@locationInput,'%')  or province LIKE CONCAT('%',@locationInput,'%')) and 
				 unitType=@unittypeInput and  genderAccommodation=@genderAccoInput and capacity=@capInput;""")
		data = cur.fetchall()
		return data		

	@classmethod
	def searchAllRentalBusiness(cls):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM rentalbusiness")
		rentalBusinesses = cur.fetchall()
		return rentalBusinesses

	@classmethod
	def searchAllUnitLocation(cls):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM locations")
		unitLocations = cur.fetchall()
		return unitLocations

	@classmethod
	def searchAllUnitImages(cls):
		cur = mysql.connection.cursor()
		cur.execute("""SELECT units.unitID,images.imageID,images.filename,images.datum 
			FROM units INNER JOIN unitimages ON units.unitID = unitimages.unitID
			INNER JOIN images
			ON unitimages.imageID = images.imageID""")
		unitImages = cur.fetchall()
		return unitImages

	@classmethod
	def searchAllunits(cls):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM units")
		data = cur.fetchall()
		return data

	@classmethod
	def renters(cls):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM renters")
		data = cur.fetchall()
		return data


