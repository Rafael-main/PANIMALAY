from flask import Flask,render_template, redirect, request,url_for,flash
from app import app

import app.accountModel as accounts
import app.profileModel as profiles
import app.addunitsModel as Addunits
import app.addpaymentsModel as Addpayments


@app.route("/signup")
def signup():
	return render_template("signup.html",title="Signup to Panimalay")

@app.route("/insertAccountAndProfile",methods=['POST','GET'])
def insertAccountAndProfile():
	if request.method == "POST":
		usernameVar = request.form['username']
		newAccount = accounts.account(username=usernameVar,email=request.form['email'],password=request.form['password'],accountType=request.form['accountType'])
		if newAccount.search(usernameVar)==True:
			return render_template("signup.html",title="Signup to Panimalay",username=usernameVar,email=request.form['email'],password=request.form['password'],accountType=request.form['accountType'],
				firstName=request.form['firstName'],lastName=request.form['lastName'],birthDate=request.form['birthDate'],gender=request.form['gender'])
		
		else:
			newProfile = profiles.profile(username=usernameVar,firstName=request.form['firstName'],lastName=request.form['lastName'],birthDate=request.form['birthDate'],gender=request.form['gender'])
			newAccount.addAccount()
			newProfile.addProfile()
			return redirect(url_for('signup'))


@app.route("/addpayments" methods = ['GET','POST'], title = 'Add Payments')
def addpayments():
	if request.method == "POST":
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		transaction = request.form['transaction']
		date = request.form['date']
		data = Addpayments.Add_Payments(firstName = firstName, lastName = lastName, transaction = transaction, date = date)
		data.addpayments()
	else:
		return render_template('addpayment.html')

@app.route("/addunits",methods=['GET','POST'], title='Add Units')
def addunits():
	if request.method == "POST":
		typee = request.form['typee']
		rate = request.form['rate']
		capacity = request.form['capacity']
		gender_accomodation = request.form['gender_accomodation']
		description = request.form['description']
		data = Addunits.Add_Units(typee = typee, rate = rate, capacity = capacity, gender_accomodation = gender_accomodation, description = description)
		data.addunits()
	else:
		return render_template('addunits.html')

