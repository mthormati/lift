from flask import Flask, render_template, url_for, request, session, redirect
from variables import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = database_name
app.config['MONGO_URI'] = database

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        #Change return to render home page
        return render_template('profile.html')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    errorMessage = ''
    #Get user information from database
    users = mongo.db.users
    loginUser = users.find_one({'username': request.form['username']})
    #Check if user exists
    if loginUser:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), loginUser['password']) == loginUser['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    errorMessage = 'Incorrect username or password'
    return render_template('index.html', errorMessage=errorMessage)

@app.route('/register', methods=['GET', 'POST'])
def register():
    #POST register user
    #GET render register.html
    errorMessage = ''
    if request.method == 'POST':
        users = mongo.db.users
        existingUser = users.find_one({'username' : request.form['username']})
        #Check if user exists
        if existingUser is None:
            #Hash password and insert user information in database
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'],
                                'password': hashpass,
                                'name': request.form['name'],
                                'weight': request.form['weight'],
                                'height': request.form['height'],
                                'experience': request.form['experience']})
            session['username'] = request.form['username']

            return redirect(url_for('index'))
        errorMessage = 'Username is taken'
        return render_template('register.html', errorMessage=errorMessage)
    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = key
    app.run(debug=True)