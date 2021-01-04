from flask import Flask,render_template, redirect, request,url_for,flash, json, jsonify, Blueprint
from app import app

from app.data import data, selected_data
import app.searchModel as searches
import app.accountModel as accounts
import app.profileModel as profiles
import app.addunitsModel as Addunits
import app.addpaymentsModel as Addpayments

@app.route('/_search_more', methods=['POST'])
def search_more():
	if request.method == 'POST':
		amenities = request.form.getlist('amenities')
		facilities = request.form.getlist('facilities')
		prop_type = request.form.getlist('PropType')
		return jsonify({'success': 'data sent'})

@app.route("/_reserve", methods=['POST'])
def reserve():
	if request.method == 'POST':
		date_of_reserve = request.form.get('date-reserve')
		return jsonify({'success':'date set'})


@app.route("/")
def index():
	return render_template("landing.html", title="PANIMALAY")

@app.route("/redirect")
def search_redirect():
	return render_template("redirect.html",title="PANIMALAY", data=data)

@app.route("/_prices", methods=['POST'])
def price_range():
	if request.method == 'POST': 
		min_price = request.form['min_price']
		max_price = request.form['max-price']

		if min_price and max_price:
			return jsonify(data)
		else:
			return jsonify({'error': 'No results available'})

@app.route("/searches/<place>")
def search_result(place):
	query = str(place)
	obj = searches.Search()
	res = obj.filter_query_by_place(query)
	if res:
		return jsonify(res)
	else:
		return jsonify({'error', 'No results available'})

@app.route("/selected/<id>")
def selected(id):
	return render_template("selected2.html",title="PANIMALAY", data=selected_data)

@app.route("/signup")
def signup():
	return render_template("signup.html",title="Signup to Panimalay")

@app.route("/redirect2")
def search_redirect2():
	return render_template("redirect2.html",title="PANIMALAY", data=data)


@app.route("/selected2")
def selected2():
	return render_template("selected2.html",title="PANIMALAY", data=selected_data)

@app.route("/api/selected")
def selected_api():
	return jsonify(data)


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

