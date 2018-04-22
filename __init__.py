from flask import Flask, render_template, url_for, request, session, redirect
from variables import *
from workout import *
from exercise import *
from search import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = database_name
app.config['MONGO_URI'] = database

mongo = PyMongo(app)

#Get user workouts parsed as a readable object
def getUserWorkouts(user):
    mdb_user_workouts = user['user_workouts']
    return parseWorkouts(mdb_user_workouts, user['name'])

def parseWorkouts(mdb_user_workouts, name):
    mdb_workouts = mongo.db.workouts
    mdb_exercises = mongo.db.exercises
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
        user_workouts.append(make_workout(mdb_user_workout, mdb_wo['title'], name, workout_exercises, mdb_wo['tags']))
        workout_num+=1
    return user_workouts

#Add friend
@app.route('/search/<ObjectId:friend_user>')
def addFriend(friend_user):
    users = mongo.db.users
    users.update( { 'username': session['username'] }, {"$push": {'user_friends': friend_user}} )
    return discovery()

#Save workout (from friends/discovery)
@app.route('/discovery/<ObjectId:workout>')
def saveWorkout(workout):
    users = mongo.db.users
    users.update( { 'username': session['username'] }, {"$push": {'user_workouts': workout}} )
    return discovery()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')
    return render_template('index.html')

@app.route('/discovery', methods=['GET'])
def discovery():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    friend_discovery_workouts = []
    for friend in user['user_friends']:
        friend_workouts = getUserWorkouts(users.find_one( {'_id': friend} ))
        for fwo in friend_workouts:
            friend_discovery_workouts.append(fwo)
    #Retrieve user workout data from data base
    return render_template('discovery.html', user_workouts=friend_discovery_workouts)

@app.route('/search', methods=['POST'])
def search():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    search = request.form['search']
    results = searchQuery(search, mongo, user)
    return render_template('search.html', users=results.users, workouts=parseWorkouts(results.workouts))

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
                                'user_workouts': [],
                                'user_friends': []})
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
