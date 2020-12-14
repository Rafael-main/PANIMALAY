from flask import Flask,render_template, redirect, request,url_for,flash
from app import app
import app.accountModel as accounts
import app.profileModel as profiles



@app.route("/signup")
def signup():
	return render_template("signup.html",title="Signup to Panimalay")

@app.route("/signin")
def signin():
	return render_template("signin.html",title="Signin to Panimalay")

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

@app.route("/login",methods=['POST','GET'])
def login():
	if request.method == "POST":
		emailOrUsername =  request.form['emailOrUsername']
		password =  request.form['password']
		loginAccount = accounts.account()
		if loginAccount.searchForLogin(emailOrUsername,password)==True:
			return "<h1>WELCOME TO YOUR DASHBOARD</h1>"
		elif loginAccount.searchForLogin(emailOrUsername,password)=="Invalid password!":
			return render_template("signin.html",title="Signin to Panimalay",errorMsg1="Invalid password!",emailOrUsername=emailOrUsername,password=password)
		else:
			return render_template("signin.html",title="Signin to Panimalay",errorMsg2="Invalid email or username",emailOrUsername=emailOrUsername,password=password)

