import base64
from app import app, mysql

class Search():
    
    @classmethod
    def selectedSearchUnit(cls, rental_id,unit_id):
        if id:
            query = """SELECT units.unitID, 
            rentalbusiness.RBID,
            units.unitID,
            rentalbusiness.rbName,
            rentalbusiness.description,
            rentalbusinessphonenumber.phoneNumber,
            units.unitType,
            units.rate,
            units.capacity,
            units.genderAccommodation


            FROM rentalbusiness 
            INNER JOIN units ON rentalbusiness.RBID = units.RBID
            INNER JOIN rentalbusinessphonenumber ON rentalbusiness.RBID = rentalbusinessphonenumber.RBID
            INNER JOIN facilities ON units.unitID = facilities.unitID 
            WHERE units.unitID = %s AND rentalbusiness.RBID = %s """

            cur = mysql.connection.cursor()
            cur.execute(query,(unit_id,rental_id))
            row_headers=[x[0] for x in cur.description]
            res = cur.fetchall()
            units = dict()
            for result in res:
                units = dict(zip(row_headers,result))
                
            return units

        else:
            return {'error': 'No results'}
            
    @classmethod
    def selectedSearchImages(cls, unit_id):
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
            blob  = base64.b64encode(result[1])
            blob = blob.decode("UTF-8")
            image_dct['datum'] = blob
            images.append(image_dct)
        return images
    @classmethod
    def selectedSearchProtocols(cls, rental_id, unit_id):
        cur = mysql.connection.cursor()
        cur.execute("""SELECT units.unitID,protocols.protocol FROM rentalbusiness
        INNER JOIN protocols ON rentalbusiness.RBID = protocols.RBID
        INNER JOIN units ON rentalbusiness.RBID = units.RBID
        WHERE rentalbusiness.RBID = %s AND units.unitID = %s""", (rental_id,unit_id))
        result = cur.fetchall()
        prtcl = list()
        for res in result:
            prtcl.append(res[1])
        return prtcl

    @classmethod
    def selectedSearchServices(cls, rental_id, unit_id):
        cur = mysql.connection.cursor()
        cur.execute("""SELECT units.unitID,services.service FROM rentalbusiness
        INNER JOIN services ON rentalbusiness.RBID = services.RBID
        INNER JOIN units ON rentalbusiness.RBID = units.RBID
        WHERE rentalbusiness.RBID = %s AND units.unitID = %s""", (rental_id,unit_id))
        result = cur.fetchall()
        srvc = list()
        for res in result:
            srvc.append(res[1])
        return srvc
        
    @classmethod
    def selectedSearchFacilities(cls, unit_id):
        cur = mysql.connection.cursor()
        cur.execute("""SELECT units.unitID,facilities.facility FROM units
        INNER JOIN facilities ON units.unitID = facilities.unitID
        WHERE units.unitID = %s""", (unit_id,))
        result = cur.fetchone()
        facilities = result[1].split(",")
        return facilities

    @classmethod
    def selectedSearchLocations(cls, unit_id):
        cur = mysql.connection.cursor()
        cur.execute("""SELECT rentalbusiness.RBID, units.unitID,locations.latitude,locations.longitude, locations.street, locations.barangay,locations.cityOrMunicipality,locations.province FROM units
        INNER JOIN locations ON units.unitID = locations.unitID
        INNER JOIN rentalbusiness ON units.RBID = rentalbusiness.RBID
        WHERE units.unitID = %s""", (unit_id,))
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        res = cur.fetchall()
        for result in res:
            location = dict(zip(row_headers,result))
            
        return location

    @classmethod
    def selectedUnitImages(cls,unit_id):
    	cur = mysql.connection.cursor()
    	cur.execute("""SELECT units.unitID,images.imageID,images.filename,images.datum 
    		FROM units INNER JOIN unitimages ON units.unitID = unitimages.unitID
    		INNER JOIN images ON unitimages.imageID = images.imageID
    		WHERE units.unitID = %s""",(unit_id,))
    	unitImages = cur.fetchall()
    	return unitImages

    @classmethod
    def selectedFeedback(cls,unit_id):
    	cur = mysql.connection.cursor()
    	cur.execute("SELECT * FROM feedbacks WHERE unitID=%s",(unit_id,))
    	feedbacks = cur.fetchall()
    	return feedbacks
	
    @classmethod
    def rentalsWithOwners(cls,rbid):
        cur = mysql.connection.cursor()
        cur.execute("SET @RBIDInput=%s",(rbid,))
        cur.execute("""SELECT * FROM (SELECT rentalbusiness.ownersUserName,rentalbusiness.rbName,rentalbusiness.RBID,rentalbusiness.description,rentalbusiness.email,profiles.firstName,profiles.lastName
        FROM rentalbusiness
        INNER JOIN profiles ON profiles.username=rentalbusiness.ownersUserName) AS rentalsandowners
        WHERE RBID=@RBIDInput;""")
        data = cur.fetchone()
        return data 
        
    @classmethod
    def selectedRentalBusiness(cls,RBID):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rentalbusiness WHERE RBID=%s",(RBID,))
        rb = cur.fetchone()
        return rb

    @classmethod
    def selectedRentalBusinessPhoneNumber(cls,RBID):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rentalbusinessphonenumber WHERE RBID=%s",(RBID,))
        phoneNumber = cur.fetchone()
        phoneNumber = phoneNumber[1]
        return phoneNumber

    @classmethod
    def selectedUnitAvailability(cls,unitID):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM renters WHERE unitID=%s",(unitID,))
        renters =  cur.fetchall()
        cur.execute("SELECT * FROM units WHERE unitID=%s",(unitID,))
        unit = cur.fetchall()
        noOfRenters = 0
        for i in renters:
            noOfRenters+=1

        if noOfRenters<unit[0][2]:
            return True
        else:
            return False

