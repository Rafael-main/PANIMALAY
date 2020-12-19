import os
import base64
from flask import Flask,render_template, redirect, request,url_for
from app import app
import app.accountModel as accounts
import app.profileModel as profiles
import app.profilepicturemodel as profilepic



	
@app.route("/signup")
def signup():
	return render_template("signup.html",title="Signup to Panimalay")

@app.route("/signin")
def signin():
	return render_template("signin.html",title="Signin to Panimalay")

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
	return render_template("profile.html",data=data,phoneNumber=phoneNumber,datum=datum)

@app.route("/updateProfilePage/<string:username>")
def updateProfilePage(username):
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
	return render_template("updateprofile.html",data=data,phoneNumber=phoneNumber,datum=datum)

@app.route("/add/profile/<string:username>/<string:profileID>",methods=["POST"])
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

@app.route("/update/profile/<string:username>/<string:profileID>",methods=["POST"])
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

@app.route("/update/info/<string:username>/<string:profileID>",methods=["POST"])
def updateInfo(username,profileID):
	if request.method == "POST":
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		gender = request.form['gender']
		accountType = request.form['accountTypeVal']
		birthDate = request.form['birthDate']
		phoneNumber = request.form['phoneNumber']
		email = request.form['email']
		password = request.form['password']
		accountToUpdate = accounts.account(username,email,password,accountType)
		profileToupdate = profiles.profile(username,firstName,lastName,birthDate,gender)
		accountToUpdate.updateAccount()
		profileToupdate.updateProfile(profileID)
		profileToupdate.updatePhoneNumber(phoneNumber,profileID)
	return redirect(url_for("updateProfilePage",username=username))



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
	return render_template("home.html",data=data,phoneNumber=phoneNumber,datum=datum)


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

