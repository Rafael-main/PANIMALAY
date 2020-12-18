from flask import Flask,render_template, redirect, request,url_for,flash, json, jsonify, Blueprint
from app import app
import app.accountModel as accounts
import app.profileModel as profiles

#data for selected.html
selected_data = {
        "unit_id": "qwe0001",
        "name-of-building":"io",
        "name-of-unit":"oi",
        "price-of-unit":"1600 php / month",
        "contact-number":"09090909090",
        "email-address": "wer3@gmail.com",
        "Property Type":["Apartments","House"],
        "location":{
            "name-of-location": "we",
            "home-number":"0001",
            "street-location":"tau",
            "barangay":"vb",
            "city/municipality":"yu",
            "region":"X",
            "country":"Phillipines",
            "postal_code": "9200",
            "coordinates": {
                "longitude": 121.7740,
                "latitude": 12.8797
            }            
            },
        "amenities": [
            "pets-allowed", "air-conditioning"
        ],
        "capacity:": [
            {
                "type":"baths",
                "maximum": "2"
            },
            {
                "type":"bed",
                "maximum": "2"
            }
        ],
        "ratings-unit":{
            "ratings-average": "5",
            "feedbacks": [
                {
                    "username": "tor",
                    "rating": "5",
                    "comments": "very good!"
                },
                {
                    "username": "tor",
                    "rating": "5",
                    "comments": "very good!",
                    "is-anonymous":"true"
                },
                {
                    "username": "tor",
                    "rating": "5",
                    "comments": "very good!",
                    "is-anonymous":"true"
                }
            ]
        },
        "unitImages": [
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            },
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            },
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            }
        ],

        "is-for": {
            "children": "yes",
            "adults": "yes"
        },
        "facilities": [
            "cafeteria"
        ]

    }


#data for redirect.html
#user_id should be unit_id mistyped :( 
data = [
    {
        "user_id":"qwe0001",
        "name-of-building":"io",
        "name-of-unit":"oi",
        "price-of-unit":"1600 php / month",
        "contact-number":"09090909090",
        "Property Type":["Apartments","House"],
        "location":{
            "name-of-location": "we",
            "home-number":"0001",
            "street-location":"tau",
            "barangay":"vb",
            "city/municipality":"yu",
            "region":"X",
            "country":"Phillipines",
            "coordinates": {
                "longitude": "121.7740",
                "latitude": "12.8797"
            }            
        },
        "capacity": [
            {
                "type":"baths",
                "maximum": "2"
            },
            {
                "type":"bed",
                "maximum": "2"
            }
        ],
        "ratings-unit":{
            "ratings-average": "5",
        },
        "unitImages": [
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            },
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            },
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            }
        ]
    },
    {
        "user_id":"qwe0001",
        "name-of-building":"io",
        "name-of-unit":"oi",
        "price-of-unit":"1600 php / month",
        "contact-number":"09090909090",
        "Property Type":["Apartments","House"],
        "location":{
            "name-of-location": "we",
            "home-number":"0001",
            "street-location":"tau",
            "barangay":"vb",
            "city/municipality":"yu",
            "region":"X",
            "country":"Phillipines",
            "coordinates": {
                "longitude": "121.7740",
                "latitude": "12.8797"
            }            
        },
        "capacity": [
            {
                "type":"baths",
                "maximum": "2"
            },
            {
                "type":"bed",
                "maximum": "2"
            }
        ],
        "ratings-unit":{
            "ratings-average": "5",
        },
        "unitImages": [
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            },
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            },
            {
                "name": "Hello",
                "image": "../static/img/pexels-alex-azabache-3727261.jpg",
                "date-of-upload": "12/16/20"
            }
        ]
    }
]

@app.route("/signup")
def signup():
	return render_template("signup.html",title="Signup to Panimalay")

@app.route("/redirect")
def search_redirect():
	return render_template("redirect.html",title="PANIMALAY", data=data)

@app.route("/selected/<id>")
def selected(id):
	return render_template("selected.html",title="PANIMALAY", data=selected_data)

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