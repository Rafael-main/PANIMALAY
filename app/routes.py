from flask import Flask,render_template, redirect, request,url_for,flash
from app import app
import app.addunitsModel as Addunits
import app.addpaymentsModel as Addpayments


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
