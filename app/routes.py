from flask import Flask,render_template, redirect, request,url_for,flash
from app import app
import app.accountModel as accounts
import app.profileModel as profiles



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