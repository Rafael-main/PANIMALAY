# #this is only for testing purposes not included in development or deployment.

# #bcrypt
# from flask import Flask
# from flask.ext.bcrypt import Bcrypt

# app = Flask(__name__)
# bcrypt = Bcrypt(app)
# pw_hash = bcrypt.generate_password_hash('hunter2')
# bcrypt.check_password_hash(pw_hash, 'hunter2') # returns True
# password = 'hunter2'
# pw_hash = bcrypt.generate_password_hash(password)
# candidate = 'secret'
# bcrypt.check_password_hash(pw_hash, candidate)