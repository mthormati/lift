from flask import Flask, render_template, url_for, request, session, redirect
from variables import *
from workout import *
from exercise import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = database_name
app.config['MONGO_URI'] = database

mongo = PyMongo(app)

#Get user workouts parsed as a readable object
def getUserWorkouts(user):
    mdb_workouts = mongo.db.workouts
    mdb_exercises = mongo.db.exercises
    mdb_user_workouts = user['user_workouts']
    user_workouts = []
    workout_num = 1
    for mdb_user_workout in mdb_user_workouts:
        mdb_wo = mdb_workouts.find_one(mdb_user_workout)
        #Parse exercies of workout
        mdb_workout_exercises = mdb_wo['exercises']
        workout_exercises = []
        exercise_num = 1
        for mdb_workout_exercise in mdb_workout_exercises:
            mdb_ex = mdb_exercises.find_one(mdb_workout_exercise)
            workout_exercises.append(make_exercise(mdb_ex['title'], mdb_ex['duration'], mdb_ex['link'], 'w'+str(workout_num)+'e'+str(exercise_num)))
            exercise_num+=1
        user_workouts.append(make_workout(mdb_wo['title'], workout_exercises, mdb_wo['tags']))
        workout_num+=1
    return user_workouts

@app.route('/')
def index():
    if 'username' in session:
        #Get user
        users = mongo.db.users
        user = users.find_one({'username': session['username']})
        #Get the user's workouts
        user_workouts = getUserWorkouts(user)

        return render_template('home.html', user_workouts=user_workouts)
    return render_template('index.html')

@app.route('/discovery', methods=['GET'])
def discovery():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})

    #Retrieve user workout data from data base
    user_workouts = getUserWorkouts(user)

    return render_template('discovery.html', user_workouts=user_workouts)

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
                                'experience': request.form['experience'],
                                'user_workouts': []})
            session['username'] = request.form['username']

            return redirect(url_for('index'))
        errorMessage = 'Username is taken'
        return render_template('register.html', errorMessage=errorMessage)
    return render_template('register.html')

@app.route('/profile', methods=['GET'])
def profile():
    #Get user
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    #Get the user's workouts
    user_workouts = getUserWorkouts(user)

    return render_template('profile.html', user=user, user_workouts=user_workouts)

if __name__ == '__main__':
    app.secret_key = key
    app.run(debug=True)
