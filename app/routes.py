
import os
from datetime import datetime
import base64
import simplejson as json
from flask import Flask,render_template, redirect, request,url_for,abort, session

from app import app
import app.accountModel as accounts
import app.profileModel as profiles
import app.profilepicturemodel as profilepic
import app.rentalbusinessmodel as renbus
import app.unitmodel as unit
import app.protocolmodel as protocol
import app.servicemodel as service
import app.paymentmodel as payments
import app.unitimagesmodel as unitimages


@app.route("/")
def guestLandingPage():
	return render_template("landingpage.html")


@app.route("/signup")
def signup():
	return render_template("signup.html",title="Signup to Panimalay")

@app.route("/signin")
def signin():
	return render_template("signin.html",title="Signin to Panimalay")


@app.route("/login",methods=['POST','GET'])
def login():
	if request.method == "POST":
		username =  request.form['username']
		password =  request.form['password']
		loginAccount = accounts.account()
		if loginAccount.searchForLogin(username,password)==True:
			acc = accounts.account()
			prof= profiles.profile()
			data = acc.profileData(username)
			phoneNumber = prof.searchPhoneNumber(username)
			file =  profilepic.profilePicture()
			datum = file.retrieveFile(data[1][1])
			if datum!=None:
				datum = base64.b64encode(datum[2])
				datum = datum.decode("UTF-8")
			else:
				datum = datum
			return redirect(url_for('home',username=username))
		elif loginAccount.searchForLogin(username,password)=="Invalid password!":
			return render_template("signin.html",title="Signin to Panimalay",errorMsg1="Invalid password!",username=username,password=password)
		else:
			return render_template("signin.html",title="Signin to Panimalay",errorMsg2="Invalid username!",username=username,password=password)

@app.route("/profile")
def profile():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		acc = accounts.account()
		prof= profiles.profile()
		data = acc.profileData(username)
		phoneNumber = prof.searchPhoneNumber(str(username))
		file =  profilepic.profilePicture()
		datum = file.retrieveFile(data[1][1])
		if datum!=None:
			datum = base64.b64encode(datum[2])
			datum = datum.decode("UTF-8")
		else:
			datum = datum
		return render_template("profile.html",data=data,phoneNumber=phoneNumber,datum=datum,username=username,accDataJSON=json.dumps(data, indent=4, sort_keys=True, default=str),accountType=accountType)
	else:
		return redirect(url_for("signin"))

@app.route("/account")
def account():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		acc = accounts.account()
		accData = acc.accountData(username)
		return render_template("account.html",username=username,accData=accData,accountType=accountType)
	else:
		return redirect(url_for("signin"))

@app.route("/account/change/email/form")
def accountChangeEmailForm():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		acc = accounts.account()
		accData = acc.accountData(username)
		accDataJSON = accData
		return render_template("accountchangeemail.html",username=username,accData=accData,accDataJSON=json.dumps(accDataJSON),accountType=accountType)
	else:
		return redirect(url_for("signin"))


@app.route("/account/change/email/<string:username>",methods=["POST"])
def accountChangeEmail(username):
	if request.method == "POST":
		newEmail = request.form["newEmail"]
		acc = accounts.account()
		acc.changeEmail(username,newEmail)
		return	redirect(url_for("account",username=username))

@app.route("/account/change/password/form")
def accountChangePasswordForm():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		acc = accounts.account()
		accData = acc.accountData(username)
		accDataJSON = accData
		return render_template("accountchangepassword.html",username=username,accData=accData,accDataJSON=json.dumps(accDataJSON),accountType=accountType)
	else:
		return redirect(url_for("signin"))

@app.route("/account/change/password/<string:username>",methods=["POST"])
def accountChangePassword(username):
	if request.method == "POST":
		newPassword = request.form["newPassword"]
		acc = accounts.account()
		acc.changePassword(username,newPassword)
		return	redirect(url_for("account",username=username))



@app.route("/update/profile/page")
def updateProfilePage():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		acc = accounts.account()
		prof= profiles.profile()
		data = acc.profileData(username)
		takenPhoneNumbers = prof.allPhoneNumbers()
		phoneNumber = prof.searchPhoneNumber(str(username))
		for t in takenPhoneNumbers:
			if t == phoneNumber[0][1]:
				takenPhoneNumbers.remove(t)
		file =  profilepic.profilePicture()
		datum = file.retrieveFile(data[1][1])
		if datum!=None:
			datum = base64.b64encode(datum[2])
			datum = datum.decode("UTF-8")
		else:
			datum = datum
		return render_template("updateprofile.html",username=username,data=data,phoneNumber=phoneNumber,datum=datum,takenPhoneNumbers=json.dumps(takenPhoneNumbers),accountType=accountType)
	else:
		return redirect(url_for("signin"))

@app.route("/add/profile/picture/<string:profileID>",methods=["POST"])
def addProfilePicture(profileID):
	file = request.files["profilePicInput"]
	filename= file.filename
	blob = file.read()
	newProfilePic = profilepic.profilePicture(filename,blob)
	newProfilePic.addProfilePicture(profileID)
	return redirect(url_for("updateProfilePage"))

@app.route("/update/profile/picture/<string:profileID>",methods=["POST"])
def updateProfilePicture(profileID):
	file = request.files["profilePicInput"]
	filename= file.filename
	blob = file.read()
	newProfilePic = profilepic.profilePicture(filename,blob)
	newProfilePic.updateProfilePicture(profileID)
	return redirect(url_for("updateProfilePage"))

@app.route("/update/profile/<string:username>/<string:profileID>",methods=["POST"])
def updateInfo(username,profileID):
	if request.method == "POST":
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		gender = request.form['gender']
		birthDate = request.form['birthDate']
		phoneNumber = request.form['phoneNumber']
		profileToupdate = profiles.profile(username,firstName,lastName,birthDate,gender)
		profileToupdate.updateProfile(profileID)
		profileToupdate.updatePhoneNumber(phoneNumber,profileID)
		return redirect(url_for("profile"))



@app.route("/insertAccountAndProfile",methods=['POST','GET'])
def insertAccountAndProfile():
	if request.method == "POST":
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		accountType = request.form['accountType']


		firstName = request.form['firstName']
		lastName = request.form['lastName']
		birthDate = request.form['birthDate']
		gender = request.form['gender']

		phoneNumber = request.form['phoneNumber']
		

		newAccount = accounts.account(username,email,password,accountType)
		newProfile = profiles.profile(username,firstName,lastName,birthDate,gender)
		
		errorMsg1 = ""

		errorMsg2 = ""
		if newAccount.usernameValidate(username)==True:
			errorMsg1 = "Username already taken!"
		if newProfile.validatePhoneNumber(phoneNumber)==True:
			errorMsg2 = "Phone number already taken!"

		if len(errorMsg1)!=0 and len(errorMsg2)==0:
			return render_template("signup.html",title="Signup to Panimalay",username=username,email=email,password=password,accountType=accountType,firstName=firstName,lastName=lastName,birthDate=birthDate,gender=gender,phoneNumber=phoneNumber,errorMsg1=errorMsg1,errorMsg2="")
		elif len(errorMsg1)==0 and len(errorMsg2)!=0:
			return render_template("signup.html",title="Signup to Panimalay",username=username,email=email,password=password,accountType=accountType,firstName=firstName,lastName=lastName,birthDate=birthDate,gender=gender,phoneNumber=phoneNumber,errorMsg1="",errorMsg2=errorMsg2)
		elif len(errorMsg1)!=0 and len(errorMsg2)!=0:
			return render_template("signup.html",title="Signup to Panimalay",username=username,email=email,password=password,accountType=accountType,firstName=firstName,lastName=lastName,birthDate=birthDate,gender=gender,phoneNumber=phoneNumber,errorMsg1=errorMsg1,errorMsg2=errorMsg2)
		else:
			newAccount.addAccount()
			newProfile.addProfile(accountType,phoneNumber)
			session["username"] = username
			session["accountType"] = accountType
			if accountType == "owner":
				return redirect(url_for('home'))
			else:
				return redirect(url_for('landingPage'))
			

@app.route("/home")
def home():
	if "username" in session:
		username = session["username"]
		acc = accounts.account()
		prof= profiles.profile()
		data = acc.profileData(username)
		phoneNumber = prof.searchPhoneNumber(str(username))
		file =  profilepic.profilePicture()
		datum = file.retrieveFile(data[1][1])
		if datum!=None:
			datum = base64.b64encode(datum[2])
			datum = datum.decode("UTF-8")
		else:
			datum = datum
		
		return render_template("home.html",username=username,data=data,phoneNumber=phoneNumber,datum=datum)
	else:
		return redirect(url_for("signin"))
	
@app.route("/manage/business")
def manageBusiness():
	if "username" in session:
		username = session["username"]
		rentalbusiness = renbus.rentalBusiness()
		if rentalbusiness.searchRentalBusiness(username)!=None:
			rentalBusinessInfo = rentalbusiness.searchRentalBusiness(username)
			RBID = rentalBusinessInfo[2]
			phoneNumber = rentalbusiness.searchRentalBusinessPhoneNumber(RBID)
			return render_template("managebusiness.html",username=username,rentalBusinessInfo=rentalBusinessInfo,phoneNumber=phoneNumber,RBID=RBID)
		else:
			return render_template("addrentalbusiness.html",username=username)
	else:
		return redirect(url_for("signin"))

@app.route("/add/rental/business/<string:username>",methods=["POST"])
def addRentalBusiness(username):
	if request.method == "POST":
		rbName = request.form["rbName"]
		email = request.form["email"]
		phoneNumber = request.form["phoneNumber"]
		description = request.form["description"]
		newRentalBusiness = renbus.rentalBusiness(username,rbName,email,phoneNumber,description)
		newRentalBusiness.addRentalBusiness()
		return redirect(url_for("manageBusiness",username=username))

@app.route("/update/rental/business/page")
def updateRentalBusinessPage():
	if "username" in session:
		username = session["username"]
		rentalbusiness = renbus.rentalBusiness()
		rentalBusinessInfo = rentalbusiness.searchRentalBusiness(username)
		RBID = rentalBusinessInfo[2]
		phoneNumber = rentalbusiness.searchRentalBusinessPhoneNumber(RBID)
		rentalBusinessInfo = rentalbusiness.searchRentalBusiness(username)
		return render_template("updaterentalbusiness.html",username=username,rentalBusinessInfo=rentalBusinessInfo,phoneNumber=phoneNumber)
	else:
		return redirect(url_for("signin"))

@app.route("/update/rental/business/<string:username>/<string:RBID>",methods=["POST"])
def updateRentalBusiness(username,RBID):
	if request.method == "POST":
		rbName = request.form["rbName"]
		email = request.form["email"]
		phoneNumber = request.form["phoneNumber"]
		description = request.form["description"]
		rentalBusiness = renbus.rentalBusiness(username,rbName,email,phoneNumber,description)
		rentalBusiness.updateRentalBusiness(RBID)
		return redirect(url_for("manageBusiness",username=username))

@app.route("/units")
def units():
	if "username" in session:
		username = session["username"]
		checkRenBus = renbus.rentalBusiness()
		ownedRenBus = checkRenBus.searchRentalBusiness(username)
		if ownedRenBus!=None:
			RBID = ownedRenBus[2]
			rbName = ownedRenBus[1]
			ownedUnits = unit.newUnit()
			ownedUnits = ownedUnits.searchUnit(RBID)
			return render_template("units.html",username=username,ownedUnits=ownedUnits,rbName=rbName,RBID=RBID)
		else:
			return render_template("units.html")
	else:
		return redirect(url_for("signin"))

@app.route("/add/unit/form")
def addUnitForm():
	if "username" in session:
		username = session["username"]
		checkRenBus = renbus.rentalBusiness()
		ownedRenBus = checkRenBus.searchRentalBusiness(username)
		if ownedRenBus!=None:
			RBID = ownedRenBus[2]
			return render_template("addunit.html",username=username,RBID=RBID)
		else:
			return render_template("addunit.html")
	else:
		return redirect(url_for("signin"))

@app.route("/add/unit",methods=["POST"])
def addUnit():
	if request.method == "POST":
		if "username" in session:
			username = session["username"]
		unitType = request.form["unitType"]
		genderAccommodation = request.form["genderAccommodation"]
		capacity = request.form["capacity"]
		rate = request.form["rate"]
		street = request.form["street"]
		barangay = request.form["barangay"]
		cityOrMunicipality = request.form["cityOrMunicipality"]
		province =request.form["province"]
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]
		facilities = request.form["facilities"]
		newUnit = unit.newUnit(username,unitType,genderAccommodation,capacity,rate,street,barangay,cityOrMunicipality,province,latitude,longitude,facilities)
		newUnit.addUnit()

	return redirect(url_for('units',username=username))

@app.route("/update/unit/form/<string:unitID>")
def updateUnitForm(unitID):
	if "username" in session:
		username = session["username"]
		ownedUnitToUpdate = unit.newUnit()
		ownedUnitToUpdateLocation = ownedUnitToUpdate.searchForUpdateUnitLocation(unitID)
		unitInfo = ownedUnitToUpdate.searchForUpdateUnit(unitID)
		ownedUnitToUpdateFacilities = ownedUnitToUpdate.searchForUpdateUnitFacilities(unitID)
		return render_template("updateunit.html",username=username,ownedUnitToUpdate=unitInfo,ownedUnitToUpdateLocation=ownedUnitToUpdateLocation,ownedUnitToUpdateFacilities=ownedUnitToUpdateFacilities)
	else:
		return redirect(url_for("signin"))

@app.route("/update/unit/<string:username>/<string:unitID>",methods=["POST"])
def updateUnit(username,unitID):
	if request.method == "POST":
		username = request.form["username"]
		unitType = request.form["unitType"]
		genderAccommodation = request.form["genderAccommodation"]
		capacity = request.form["capacity"]
		rate = request.form["rate"]
		street = request.form["street"]
		barangay = request.form["barangay"]
		cityOrMunicipality = request.form["cityOrMunicipality"]
		province =request.form["province"]
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]
		facilities = request.form["facilities"]
		unitToUpdate = unit.newUnit(username,unitType,genderAccommodation,capacity,rate,street,barangay,cityOrMunicipality,province,latitude,longitude,facilities)
		unitToUpdate.updateUnit(unitID)
		return redirect(url_for("units",username=username))

@app.route("/delete/unit/<string:unitID>")
def deleteUnit(unitID):
	if "username" in session:
		username = session["username"]
		ownedUnitToDelete = unit.newUnit()
		ownedUnitToDelete.delUnit(unitID)
		return redirect(url_for("units",username=username))
	else:
		return redirect(url_for("signin"))

@app.route("/business/protocols/<string:RBID>")
def protocols(RBID):
	if "username" in session:
		username = session["username"]
		businessProtocol = protocol.newProtocol()
		businessProtocol = businessProtocol.searchProtocols(RBID)
		return render_template("protocols.html",username=username,RBID=RBID,protocols=businessProtocol)
	else:
		return redirect(url_for("signin"))

@app.route("/add/protocol/<string:username>/<string:RBID>",methods=["POST"])
def addProtocol(username,RBID):
	if request.method == "POST":
		protocolTobeAdded = request.form["protocol"]
		businessProtocol = protocol.newProtocol(protocolTobeAdded,RBID)
		businessProtocol.addProtocol()
		return redirect(url_for("protocols",username=username,RBID=RBID))

@app.route("/update/protocol/<string:username>/<string:RBID>/<int:protocolNo>",methods=["POST"])
def updateProtocol(username,RBID,protocolNo):
	if request.method == "POST":
		protocolTobeUpdated = request.form["protocol"]
		businessProtocol = protocol.newProtocol()
		businessProtocol.updatePrtcl(protocolTobeUpdated,protocolNo)
		return redirect(url_for("protocols",username=username,RBID=RBID))

@app.route("/delete/protocol/<string:username>/<string:RBID>/<int:protocolNo>",methods=["POST"])
def deleteProtocol(username,RBID,protocolNo):
	if request.method == "POST":
		businessProtocol = protocol.newProtocol()
		businessProtocol.deletePrtcl(protocolNo)
	return redirect(url_for("protocols",username=username,RBID=RBID))

@app.route("/business/services/<string:RBID>")
def services(RBID):
	if "username" in session:
		username = session["username"]
		businessServices = service.newServices()
		businessServices = businessServices.searchServices(RBID)
		return render_template("services.html",username=username,RBID=RBID,services=businessServices)
	else:
		return redirect(url_for(signin))

@app.route("/add/service/<string:username>/<string:RBID>",methods=["POST"])
def addService(username,RBID):
	if request.method == "POST":
		serviceTobeAdded = request.form["service"]
		businessServices = service.newServices(serviceTobeAdded,RBID)
		businessServices.addService()
		return redirect(url_for("services",username=username,RBID=RBID))

@app.route("/update/service/<string:username>/<string:RBID>/<int:serviceNo>",methods=["POST"])
def updateService(username,RBID,serviceNo):
	if request.method == "POST":
		serviceTobeUpdate = request.form["service"]
		businessServices = service.newServices()
		businessServices.updateSrvc(serviceTobeUpdate,serviceNo)
		return redirect(url_for("services",username=username,RBID=RBID))

@app.route("/delete/service/<string:username>/<string:RBID>/<int:serviceNo>",methods=["POST"])
def deleteService(username,RBID,serviceNo):
	if request.method == "POST":
		businessServices = service.newServices()
		businessServices.deleteSrvc(serviceNo)
		return redirect(url_for("services",username=username,RBID=RBID))

@app.route("/payments")
def paymentsTable():
	if "username" in session:
		username = session["username"]
		RBID = renbus.rentalBusiness()
		RBID = RBID.searchRentalBusiness(username)
		if RBID!=None:
			RBID = RBID[2]
			ownedUnits = unit.newUnit()
			ownedUnits = ownedUnits.searchUnit(RBID)
			paymentRecord =  payments.newPayment()
			paymentRecord = paymentRecord.searchPayments(RBID)
			return render_template("payment.html",username=username,RBID=RBID,ownedUnits=ownedUnits,paymentRecord=paymentRecord)
		else:
			return redirect(url_for("manageBusiness"))
	else:
		return redirect(url_for("signin"))

@app.route("/add/payment/<string:username>/<string:RBID>",methods=["POST"])
def Payment(username,RBID):
	if request.method =="POST":
		payersUsername  = request.form["username"]
		amount = request.form["amount"]
		unitRented = request.form["unitRented"]
		paymentDate = request.form["paymentDate"]
		pay = payments.newPayment(payersUsername,amount,paymentDate,unitRented)
		pay.addPayment(RBID)
		return redirect(url_for("paymentsTable",username=username))

@app.route("/update/payment/<string:username>/<int:paymentNo>",methods=["POST"])
def updatePayment(username,paymentNo):
	if request.method =="POST":
		payersUsername  = request.form["username"]
		amount = request.form["amount"]
		unitRented = request.form["unitRented"]
		paymentDate = request.form["paymentDate"]
		paymentToUpdate = payments.newPayment(payersUsername,amount,paymentDate,unitRented)
		paymentToUpdate.updatePayment(paymentNo)
		return redirect(url_for("paymentsTable",username=username))

@app.route("/delete/payment/<string:username>/<int:paymentNo>",methods=["POST"])
def delPayment(username,paymentNo):
	if request.method =="POST":
		paymentToDelete = payments.newPayment()
		paymentToDelete.deletePayment(paymentNo)
		return redirect(url_for("paymentsTable",username=username))

@app.route("/unit/gallery/<string:unitID>")
def gallery(unitID):
	if "username" in session:
		username = session["username"]
		RBID = renbus.rentalBusiness()
		RBID = RBID.searchRentalBusiness(username)
		RBID = RBID[2]
		images = unitimages.unitImages()
		images = images.searchImages(unitID)
		imageChecker = len(images)
		imagesBlob = []
		if imageChecker!=0:
			for image in images:
				blob  = base64.b64encode(image[2])
				blob = blob.decode("UTF-8")
				imagesBlob.append([image[0],blob])	
		return render_template("unitimagesgallery.html",username=username,unitID=unitID,imagesBlob=imagesBlob,RBID=RBID,imageChecker=imageChecker)
	else:
		return redirect(url_for("signin"))

@app.route("/upload/unit/images/<string:username>/<string:unitID>",methods=["POST"])
def uploadUnitImages(username,unitID):
	if request.method == "POST":
		files = request.files.getlist("unitImages[]")
		for file in files:
			filename = file.filename
			blob = file.read()
			newImage = unitimages.unitImages(filename,blob)
			newImage.addImage(unitID)
	return redirect(url_for("gallery",unitID=unitID))

@app.route("/delete/unit/image/<string:unitID>/<string:imageID>")
def deleteUnitImage(unitID,imageID):
	if "username" in session:
		username = session["username"]
		delImage = unitimages.unitImages()
		delImage.deleteImages(imageID)
		return redirect(url_for("gallery",unitID=unitID))
	else:
		return redirect(url_for("signin"))

@app.route("/search/result",methods=["GET","POST"])
def searchResult():
	if request.method =="POST":
		location = request.form["location"]
		unitType = request.form["unitType"]
		genderAccommodation = request.form["genderAccommodation"]
		capacity = request.form["capacity"]
		searchUnit = unit.newUnit()
		allUnits = searchUnit.searchResult(location,unitType,genderAccommodation,capacity)
		rentalBusinesses = searchUnit.searchAllRentalBusiness()
		unitLocations = searchUnit.searchAllUnitLocation()
		unitImages = searchUnit.searchAllUnitImages()
		imagesBlob = []
		imageChecker = len(unitImages)
		if imageChecker!=0:
			for image in unitImages:
				blob  = base64.b64encode(image[3])
				blob = blob.decode("UTF-8")
				imagesBlob.append([image[0],image[1],image[2],blob])
		if "username" in session and "accountType" in session:
			username = session["username"]
			accountType = session["accountType"]
			currentDate = datetime.today().strftime('%Y-%m-%d')
			return render_template("searchResult.html",allUnits=allUnits,rentalBusinesses=rentalBusinesses,unitLocations=unitLocations,imagesBlob=imagesBlob,allUnitsJSON=json.dumps(allUnits),rentalBusinessesJSON=json.dumps(rentalBusinesses),unitLocationsJSON=json.dumps(unitLocations),username=username,accountType=accountType,currentDate=currentDate)
		else:
			return render_template("searchResult.html",allUnits=allUnits,rentalBusinesses=rentalBusinesses,unitLocations=unitLocations,imagesBlob=imagesBlob,allUnitsJSON=json.dumps(allUnits),rentalBusinessesJSON=json.dumps(rentalBusinesses),unitLocationsJSON=json.dumps(unitLocations))	
	else:
		if "username" in session and "accountType" in session:
			username = session["username"]
		return render_template("searchResult.html",username=username)

@app.route("/feedback/<string:unitID>")
def feedbackForm(unitID):
	if "username" in session:
		username = session["username"]
		feedBackandRatings =  feedback.newFeedback()
		feedbacks = feedBackandRatings.searchAllFeedback(unitID)
		profileInfo=profiles.profile()
		profileInfo  = profileInfo.searchProfile(username)
		return render_template("feedback.html",username=username,unitID=unitID,feedbacks=feedbacks,profileInfo=profileInfo)
	else:
		return render_template("feedback.html")

@app.route("/add/feedback/<string:unitID>/<string:RBID>",methods=["POST"])
def addFeedback(unitID,RBID):
	if request.method == "POST":
		comment = request.form["comment"]
		starRating = request.form["starRating"]
		feedbackDate = request.form["feedbackDate"]   
		if "username" in session:
			username = session["username"]
			feedBackandRatings = feedback.newFeedback(username,unitID,starRating,comment,feedbackDate)
			feedBackandRatings.add()
			return	redirect(url_for("selected_unit",RBID=RBID,unitID=unitID))
	else:
		return	redirect(url_for("selected_unit",RBID=RBID,unitID=unitID))

@app.route("/update/feedback/<string:unitID>/<string:RBID>/<int:feedbackNo>",methods=["POST"])
def updateFeedback(unitID,RBID,feedbackNo):
	if request.method == "POST":
		comment = request.form["comment"]
		starRating = request.form["starRating"]
		feedbackDate = request.form["feedbackDate"]   
		if "username" in session:
			username = session["username"]
			feedBackandRatings = feedback.newFeedback()
			feedBackandRatings.updateFeedback(comment,starRating,feedbackDate,feedbackNo)
			return	redirect(url_for("selected_unit",RBID=RBID,unitID=unitID))
	else:
		return	redirect(url_for("selected_unit",RBID=RBID,unitID=unitID))

@app.route("/delete/feedback/<string:unitID>/<string:RBID>/<int:feedbackNo>")
def deleteFeedback(unitID,RBID,feedbackNo):  
	if "username" in session:
		username = session["username"]
		feedBackandRatings = feedback.newFeedback()
		feedBackandRatings.deleteFeedback(feedbackNo)
		return	redirect(url_for("selected_unit",RBID=RBID,unitID=unitID))
	else:
		return	redirect(url_for("selected_unit",RBID=RBID,unitID=unitID))


@app.route("/renters")
def renters():
	if "username" in session:
		username = session["username"]
		rentalbusiness = renbus.rentalBusiness()
		rentalBusinessInfo = rentalbusiness.searchRentalBusiness(username)
		if rentalbusiness.searchRentalBusiness(username)!=None:
			RBID = rentalBusinessInfo[2]
			ownedUnits = unit.newUnit()
			rentersInfo = ownedUnits.renterInfo()
			profilePictures = profilepic.profilePicture()
			profilePictures = profilePictures.searchAllProfilePictures()
			profilePicturesWithBlob = []
			imageChecker = len(profilePictures)
			if imageChecker!=0:
				for picture in profilePictures:
					blob  = base64.b64encode(picture[3])
					blob = blob.decode("UTF-8")
					profilePicturesWithBlob.append([picture[0],picture[1],picture[2],blob])

			return render_template("renters.html",RBID=RBID,rentersInfo=rentersInfo,profilePictures=profilePicturesWithBlob)
		else:
			return redirect(url_for("manageBusiness"))
	else:
		return redirect(url_for("signin"))

@app.route("/renter/reservations")
def rentersReservations():
	if "username" in session:
		username = session["username"]
		allReservations = reservation.newReservation()
		allReservations=allReservations.searchReservations()
		allUnits = unit.newUnit()
		rentalBusinesses = allUnits.searchAllRentalBusiness()
		unitLocations = allUnits.searchAllUnitLocation()
		allUnits = allUnits.searchAllunits()
		rb = renbus.rentalBusiness()
		phoneNumbers = rb.searchAllRentalBusinessPhoneNumber()
		return render_template("renterreservation.html",allReservations=allReservations,allUnits=allUnits,rentalBusinesses=rentalBusinesses,unitLocations=unitLocations,username=username,phoneNumbers=phoneNumbers)
	else:
		return redirect(url_for("signin"))


@app.route("/owner/reservations")
def ownersReservation():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		if accountType == "owner":
			allReservations = reservation.newReservation()
			allReservations=allReservations.searchReservations()
			allUnits = unit.newUnit()
			allProfiles = profiles.profile()
			renterPhoneNumbers = allProfiles.allPhoneNumberWithID()
			allProfiles = allProfiles.allProfiles()
			rentalBusinesses = allUnits.searchAllRentalBusiness()
			unitLocations = allUnits.searchAllUnitLocation()
			allUnits = allUnits.searchAllunits()
			checkRenBus = renbus.rentalBusiness()
			ownedRenBus = checkRenBus.searchRentalBusiness(username)
			if ownedRenBus!=None:
				RBID = ownedRenBus[2]
				rbName = ownedRenBus[1]
				ownedUnits = unit.newUnit()
				ownedUnits = ownedUnits.searchUnit(RBID)
				return render_template("ownerreservation.html",RBID=RBID,rbName=rbName,ownedUnits=ownedUnits,allReservations=allReservations,allUnits=allUnits,rentalBusinesses=rentalBusinesses,unitLocations=unitLocations,username=username,allProfiles=allProfiles,renterPhoneNumbers=renterPhoneNumbers)
			else:
				return redirect(url_for("manageBusiness"))
	else:
		return redirect(url_for("signin"))

@app.route("/add/reservation/<string:unitID>",methods=["POST"])
def addReservation(unitID):
	if request.method== "POST":
		if "username" in session:
			username = session["username"]
			reservationDate = datetime.today().strftime('%Y-%m-%d')
			newReservation = reservation.newReservation(username,unitID,reservationDate)
			newReservation.addReservation()
			return redirect(url_for("rentersReservations"))
		else:
			return redirect(url_for("signin"))
	else:
		return redirect(url_for("signin"))

@app.route("/accept/reservation/<int:reservationNo>")
def acceptReservation(reservationNo):
	if "username" in session:
			username = session["username"]
			accountType = session["accountType"]
			if accountType == "owner":
				newReservation = reservation.newReservation()
				newReservation.accept(reservationNo)
				flash(u'You have accepted the reservation!','success')
			return redirect(url_for("ownersReservation"))
	else:
		return redirect(url_for("landingPage"))


@app.route("/decline/reservation/<int:reservationNo>")
def declineReservation(reservationNo):
	if "username" in session:
			username = session["username"]
			accountType = session["accountType"]
			if accountType == "owner":
				newReservation = reservation.newReservation()
				newReservation.decline(reservationNo)
				flash(u'You have declined the reservation!','success')
			return redirect(url_for("ownersReservation"))
	else:
		redirect(url_for("landingPage"))

@app.route("/delete/reservation/<int:reservationNo>")
def deleteReservation(reservationNo):
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		if accountType == "renter":
			newReservation = reservation.newReservation()
			newReservation.deleteReservation(reservationNo)
			flash(u'You have delete the reservation!','success')
		return redirect(url_for("rentersReservations"))
	else:
		return redirect(url_for("landingPage"))

@app.route("/confirm/reservation/<int:reservationNo>/<string:unitID>")
def confirmReservation(reservationNo,unitID):
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		if accountType == "renter":
			confirmedReservation = reservation.newReservation()
			confirmedReservation.confirm(reservationNo,username,unitID)
		return redirect(url_for("rentersReservations"))
	else:
		return redirect(url_for("landingPage"))

@app.route("/rented/unit")
def rentedUnit():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		if accountType == "renter":
			searchAllRenters = unit.newUnit()
			rentals = searchAllRenters.searchAllRentalBusiness()
			allUnits =searchAllRenters.searchAllunits()
			locations = searchAllRenters.searchAllUnitLocation()
			renters = searchAllRenters.renters()
			rb = renbus.rentalBusiness()
			phoneNumbers = rb.searchAllRentalBusinessPhoneNumber()
			return render_template("rentedunit.html",username=username,accountType=accountType,rentals=rentals,locations=locations,renters=renters,units=allUnits,phoneNumbers=phoneNumbers)
	else:
		return redirect(url_for("landingPage"))

@app.route("/reviewed/units")
def reviewUnits():
	if "username" in session:
		username = session["username"]
		accountType = session["accountType"]
		if accountType == "renter":
			allUnits = unit.newUnit()
			rentals = allUnits.searchAllRentalBusiness()
			allUnits = allUnits.searchAllunits()
			rb = renbus.rentalBusiness()
			phoneNumbers = rb.searchAllRentalBusinessPhoneNumber()
			feedBackandRatings =  feedback.newFeedback()
			feedbacks = feedBackandRatings.reviewedUnitsFeedback()
		return render_template("reviewedunits.html",username=username,accountType=accountType,rentals=rentals,units=allUnits,feedbacks=feedbacks)
	else:
		return redirect(url_for("landingPage"))
@app.route("/signout")

def logout():
	if "username" in session:
		session.pop("username",None)
		session.pop("accountType",None)
		return redirect(url_for("signin"))
	else:
		return redirect(url_for("signin"))	

@app.route('/selected/unit/<string:RBID>/<string:unitID>')
def selected_unit(RBID,unitID):

	res = searches.Search()
	searchResultUnits = res.selectedSearchUnit(RBID, unitID)
	searchResultProtocols = res.selectedSearchProtocols(RBID, unitID)
	searchResultServices = res.selectedSearchServices(RBID,unitID)
	searchResultFacilities = res.selectedSearchFacilities(unitID)
	searchResultLocations = res.selectedSearchLocations(unitID)
	searchResultAvailability = res.selectedUnitAvailability(unitID)
	searchResultUnitImages = res.selectedUnitImages(unitID)
	searchResultRentalBusiness = res.selectedRentalBusiness(RBID)
	searchResultRentalBusinessPhoneNumber = res.selectedRentalBusinessPhoneNumber(RBID)
	searchResultFeedback = feedback.newFeedback()
	searchResultFeedback = searchResultFeedback.searchAllFeedback(unitID)
	userProfiles = profiles.profile()  
	allProfiles = userProfiles.allProfiles()
	imagesBlob = []
	imageChecker = len(searchResultUnitImages)
	if imageChecker!=0:
		for image in searchResultUnitImages:
			blob  = base64.b64encode(image[3])
			blob = blob.decode("UTF-8")
			imagesBlob.append([image[0],image[1],image[2],blob])
	if "username" in session:
		username = session["username"]
	else:
		username = "unknown"

	#calculate the average star rating
	sumOfAllStar = 0
	if len(searchResultFeedback)!=0:
		for f in searchResultFeedback:
				sumOfAllStar = sumOfAllStar + f[4]
		starRatingAverage = sumOfAllStar/len(searchResultFeedback)
	else:
		starRatingAverage = sumOfAllStar
	#current data
	currentDate = datetime.today().strftime('%Y-%m-%d')

	currentUserFeedbackChecker = 0
	if searchResultFeedback!=None:
		for i in searchResultFeedback:
			if i[0]==username:
				currentUserFeedbackChecker = 1


	searchResultUnits['locations'] = searchResultLocations
	searchResultUnits['protocols'] = searchResultProtocols
	searchResultUnits['services'] = searchResultServices
	searchResultUnits['facilities'] = searchResultFacilities
	searchResultUnits['images'] = imagesBlob
	searchResultUnits['rental'] = searchResultRentalBusiness
	searchResultUnits['phonenumber'] = searchResultRentalBusinessPhoneNumber
	searchResultUnits['profiles'] = allProfiles
	searchResultUnits['feedbacks'] = searchResultFeedback
	searchResultUnits['currentUserFeedbackChecker'] = currentUserFeedbackChecker
	searchResultUnits['starRatingAverage'] = starRatingAverage
	searchResultUnits['currentDate'] = currentDate
	searchResultUnits['searchResultAvailability'] = searchResultAvailability 

	return render_template('selected.html', selected_data=searchResultUnits,RBID=RBID,unitID=unitID,username=username)
