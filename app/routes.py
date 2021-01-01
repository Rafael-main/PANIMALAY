import json
import base64
from flask import Flask,render_template, redirect, request,url_for,abort
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

@app.route("/profile/<string:username>")
def profile(username):
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
	return render_template("profile.html",data=data,phoneNumber=phoneNumber,datum=datum,username=username,accDataJSON=json.dumps(data, indent=4, sort_keys=True, default=str))
@app.route("/account/<string:username>")
def account(username):
	acc = accounts.account()
	accData = acc.accountData(username)
	return render_template("account.html",username=username,accData=accData)

@app.route("/account/change/email/form/<string:username>")
def accountChangeEmailForm(username):
	acc = accounts.account()
	accData = acc.accountData(username)
	accDataJSON = accData
	return render_template("accountchangeemail.html",username=username,accData=accData,accDataJSON=json.dumps(accDataJSON))

@app.route("/account/change/email/<string:username>",methods=["POST"])
def accountChangeEmail(username):
	if request.method == "POST":
		newEmail = request.form["newEmail"]
		acc = accounts.account()
		acc.changeEmail(username,newEmail)
		return	redirect(url_for("account",username=username))

@app.route("/account/change/password/form/<string:username>")
def accountChangePasswordForm(username):
	acc = accounts.account()
	accData = acc.accountData(username)
	accDataJSON = accData
	return render_template("accountchangepassword.html",username=username,accData=accData,accDataJSON=json.dumps(accDataJSON))

@app.route("/account/change/password/<string:username>",methods=["POST"])
def accountChangePassword(username):
	if request.method == "POST":
		newPassword = request.form["newPassword"]
		acc = accounts.account()
		acc.changePassword(username,newPassword)
		return	redirect(url_for("account",username=username))



@app.route("/update/profile/page/<string:username>")
def updateProfilePage(username):
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
	return render_template("updateprofile.html",username=username,data=data,phoneNumber=phoneNumber,datum=datum,takenPhoneNumbers=json.dumps(takenPhoneNumbers))

@app.route("/add/profile/picture/<string:username>/<string:profileID>",methods=["POST"])
def addProfilePicture(username,profileID):
	file = request.files["profilePicInput"]
	filename= file.filename
	blob = file.read()
	newProfilePic = profilepic.profilePicture(filename,blob)
	newProfilePic.addProfilePicture(profileID)
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
	return redirect(url_for("updateProfilePage",username=username,data=data,phoneNumber=phoneNumber,datum=datum))

@app.route("/update/profile/picture/<string:username>/<string:profileID>",methods=["POST"])
def updateProfilePicture(username,profileID):
	file = request.files["profilePicInput"]
	filename= file.filename
	blob = file.read()
	newProfilePic = profilepic.profilePicture(filename,blob)
	newProfilePic.updateProfilePicture(profileID)
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
	return redirect(url_for("updateProfilePage",username=username,data=data,phoneNumber=phoneNumber,datum=datum))

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
		return redirect(url_for("profile",username=username))



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
			return redirect(url_for('home',username=username))
			

@app.route("/home/<string:username>")
def home(username):
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
	if data[0][3]=="owner":
		return render_template("home.html",username=username,data=data,phoneNumber=phoneNumber,datum=datum)
	else:
		return '<h1>WELCOME TO RENTER DASHBOARD/h1>'

@app.route("/manage/business/<string:username>")
def manageBusiness(username):
	rentalbusiness = renbus.rentalBusiness()
	if rentalbusiness.searchRentalBusiness(username)!=None:
		rentalBusinessInfo = rentalbusiness.searchRentalBusiness(username)
		RBID = rentalBusinessInfo[2]
		phoneNumber = rentalbusiness.searchRentalBusinessPhoneNumber(RBID)
		return render_template("managebusiness.html",username=username,rentalBusinessInfo=rentalBusinessInfo,phoneNumber=phoneNumber,RBID=RBID)
	else:
		return render_template("addrentalbusiness.html",username=username)
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
@app.route("/update/rental/business/page/<string:username>")
def updateRentalBusinessPage(username):
	rentalbusiness = renbus.rentalBusiness()
	rentalBusinessInfo = rentalbusiness.searchRentalBusiness(username)
	RBID = rentalBusinessInfo[2]
	phoneNumber = rentalbusiness.searchRentalBusinessPhoneNumber(RBID)
	return render_template("updaterentalbusiness.html",username=username,rentalBusinessInfo=rentalBusinessInfo,phoneNumber=phoneNumber)

	rentalBusinessInfo = rentalbusiness.searchRentalBusiness(username)
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

@app.route("/units/of/<string:username>")
def units(username):
	checkRenBus = renbus.rentalBusiness()
	ownedRenBus = checkRenBus.searchRentalBusiness(username)
	if ownedRenBus!=None:
		RBID = ownedRenBus[2]
		rbName = ownedRenBus[1]
		ownedUnits = unit.newUnit()
		ownedUnits = ownedUnits.searchUnit(RBID)

		return render_template("units.html",username=username,ownedUnits=ownedUnits,rbName=rbName,RBID=RBID
			)
	else:
		return render_template("units.html",username=username)

@app.route("/add/unit/form/<string:username>")
def addUnitForm(username):
	checkRenBus = renbus.rentalBusiness()
	ownedRenBus = checkRenBus.searchRentalBusiness(username)
	if ownedRenBus!=None:
		RBID = ownedRenBus[2]
		return render_template("addunit.html",username=username,RBID=RBID)
	else:
		return render_template("addunit.html",username=username)

@app.route("/add/unit",methods=["POST"])
def addUnit():
	if request.method == "POST":
		username = request.form["username"]
		unitType = request.form["unitType"]
		genderAccommodation = request.form["genderAccommodation"]
		capacity = request.form["capacity"]
		rate = request.form["rate"]
		street = request.form["street"]
		barangay = request.form["barangay"]
		city = request.form["city"]
		zipcode =request.form["zipcode"]
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]
		facilities = request.form["facilities"]
		newUnit = unit.newUnit(username,unitType,genderAccommodation,capacity,rate,street,barangay,city,zipcode,latitude,longitude,facilities)
		newUnit.addUnit()

	return redirect(url_for('units',username=username))

@app.route("/update/unit/form/<string:username>/<string:unitID>")
def updateUnitForm(username,unitID):
	ownedUnitToUpdate = unit.newUnit()
	ownedUnitToUpdateLocation = ownedUnitToUpdate.searchForUpdateUnitLocation(unitID)
	unitInfo = ownedUnitToUpdate.searchForUpdateUnit(unitID)
	ownedUnitToUpdateFacilities = ownedUnitToUpdate.searchForUpdateUnitFacilities(unitID)
	return render_template("updateunit.html",username=username,ownedUnitToUpdate=unitInfo,ownedUnitToUpdateLocation=ownedUnitToUpdateLocation,ownedUnitToUpdateFacilities=ownedUnitToUpdateFacilities)

@app.route("/update/unit/<string:username>/<string:unitID>",methods=["POST"])
def updateUnit(username,unitID):
	if request.method == "POST":
		sername = request.form["username"]
		unitType = request.form["unitType"]
		genderAccommodation = request.form["genderAccommodation"]
		capacity = request.form["capacity"]
		rate = request.form["rate"]
		street = request.form["street"]
		barangay = request.form["barangay"]
		city = request.form["city"]
		zipcode =request.form["zipcode"]
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]
		facilities = request.form["facilities"]
		unitToUpdate = unit.newUnit(username,unitType,genderAccommodation,capacity,rate,street,barangay,city,zipcode,latitude,longitude,facilities)
		unitToUpdate.updateUnit(unitID)
		return redirect(url_for("units",username=username))

@app.route("/business/protocols/<string:username>/<string:RBID>")
def protocols(username,RBID):
	businessProtocol = protocol.newProtocols()
	businessProtocol = businessProtocol.searchProtocol(RBID)
	return render_template("protocols.html",username=username,RBID=RBID,protocol=businessProtocol)

@app.route("/add/protocol/<string:username>/<string:RBID>",methods=["POST"])
def addProtocol(username,RBID):
	if request.method == "POST":
		protocolTobeAdded = request.form["protocols"]
		businessProtocol = protocol.newProtocols(protocolTobeAdded,RBID)
		businessProtocol.addProtocols()
		return redirect(url_for("protocols",username=username,RBID=RBID))

@app.route("/update/protocol/<string:username>/<string:RBID>",methods=["POST"])
def updateProtcol(username,RBID):
	if request.method == "POST":
		protocolTobeUpdated = request.form["protocols"]
		businessProtocol = protocol.newProtocols(protocolTobeUpdated,RBID)
		businessProtocol.updateProtocols()
		return redirect(url_for("protocols",username=username,RBID=RBID))

@app.route("/business/services/<string:username>/<string:RBID>")
def services(username,RBID):
	businessServices = service.newServices()
	businessServices = businessServices.searchServices(RBID)
	return render_template("services.html",username=username,RBID=RBID,service=businessServices)

@app.route("/add/service/<string:username>/<string:RBID>",methods=["POST"])
def addServices(username,RBID):
	if request.method == "POST":
		serviceTobeAdded = request.form["services"]
		businessServices = service.newServices(serviceTobeAdded,RBID)
		businessServices.addServices()
		return redirect(url_for("services",username=username,RBID=RBID))
@app.route("/update/service/<string:username>/<string:RBID>",methods=["POST"])
def updateServices(username,RBID):
	if request.method == "POST":
		serviceTobeUpdate = request.form["services"]
		businessServices = service.newServices(serviceTobeUpdate,RBID)
		businessServices.updateServices()
		return redirect(url_for("services",username=username,RBID=RBID))

@app.route("/payments/<string:username>")
def paymentsTable(username):
	RBID = renbus.rentalBusiness()
	RBID = RBID.searchRentalBusiness(username)
	RBID = RBID[2]
	ownedUnits = unit.newUnit()
	ownedUnits = ownedUnits.searchUnit(RBID)
	paymentRecord =  payments.newPayment()
	paymentRecord = paymentRecord.searchPayments(RBID)
	return render_template("payment.html",username=username,RBID=RBID,ownedUnits=ownedUnits,paymentRecord=paymentRecord)

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

@app.route("/unit/gallery/<string:username>/<string:unitID>")
def gallery(username,unitID):
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

@app.route("/upload/unit/images/<string:username>/<string:unitID>",methods=["POST"])
def uploadUnitImages(username,unitID):
	if request.method == "POST":
		files = request.files.getlist("unitImages[]")
		for file in files:
			filename = file.filename
			blob = file.read()
			newImage = unitimages.unitImages(filename,blob)
			newImage.addImage(unitID)
	return redirect(url_for("gallery",username=username,unitID=unitID))

@app.route("/delete/unit/image/<string:username>/<string:imageID>")
def deleteUnitImage(imageID):
	delImage = unitimages.unitImages()
	delImage.deleteImages(imageID)
	return redirect(url_for("gallery",username=username,unitID=unitID))


