from flask import Flask, render_template, url_for, request, session, redirect, send_file, flash
from variables import *
from workout import *
from exercise import *
from search import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt, os
import codecs
import random
import logging

app = Flask(__name__)

app.config['MONGO_DBNAME'] = database_name
app.config['MONGO_URI'] = database

mongo = PyMongo(app)

#Get user workouts parsed as a readable object
def getUserWorkouts(user):
    mdb_user_workouts = user['active_workouts']
    return parseWorkouts(mdb_user_workouts, user['name'], user)

def parseWorkouts(mdb_user_workouts, name, user):
    mdb_workouts = mongo.db.workouts
    mdb_exercises = mongo.db.exercises
    user_workouts = []
    workout_num = 1
    for mdb_user_workout in mdb_user_workouts:
        mdb_wo = mdb_workouts.find_one(mdb_user_workout)
        #Parse exercise of workout
        mdb_workout_exercises = mdb_wo['exercises']
        workout_exercises = []
        exercise_num = 1
        for mdb_workout_exercise in mdb_workout_exercises:
            mdb_ex = mdb_exercises.find_one(mdb_workout_exercise)
            workout_exercises.append(make_exercise(mdb_ex['title'],
                                                      mdb_ex['duration'],
                                                      mdb_ex['link'],
                                                      'w'+str(workout_num)+'e'+str(exercise_num),
                                                      mdb_ex['_id'],))
            exercise_num+=1
        user_workouts.append(make_workout(mdb_wo['title'],
                                           name,
                                           workout_exercises,
                                           mdb_wo['tags'],
                                           mdb_wo['_id'],
                                           getProfilePicture(user)))
        workout_num+=1
    return user_workouts

#Takes in a user as a param
#Returns the data for the image of the profile picture
def getProfilePicture(user):
    fileCollection = mongo.db['fs.files']
    existingFile = fileCollection.find_one({'filename': user['username']})
    image = None
    if existingFile is not  None:
        file_data = mongo.send_file(user['username'])
        file_data.direct_passthrough = False
        base64_data = codecs.encode(file_data.data, 'base64')
        image = base64_data.decode('utf-8')
    return image

#Add friend
@app.route('/search/add/<ObjectId:friend_user>', methods=['POST'])
def addFriend(friend_user):
    users = mongo.db.users
    users.update( { 'username': session['username'] }, {"$push": {'user_friends': friend_user}} )
    return redirect(url_for('discovery'))

@app.route('/search/remove/<ObjectId:friend_user>', methods=['POST'])
def removeFriend(friend_user):
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    #Find index of friend in user_friends
    for index, friend in enumerate(user['user_friends']):
        if friend == friend_user:
            friend_index = index
            break
    #Remove friend from user_friends
    key = 'user_friends.' + str(friend_index)
    users.find_one_and_update({ 'username': session['username'] }, { '$unset' : { key : 1 } })
    users.find_one_and_update({ 'username': session['username'] }, { '$pull' : { 'user_friends' : None } })
    return redirect(url_for('discovery'))

#TODO: UPDATE TO ADD WORKOUT TO ACTIVE WORKOUTS
#Save workout (from friends/discovery)
@app.route('/<request_path>/<ObjectId:workout>')
def saveWorkout(request_path, workout):
    users = mongo.db.users
    users.update( { 'username': session['username'] }, {"$push": {'user_workouts': workout}} )
    if request_path == 'profile':
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('discovery'))

#TODO: MOVE WORKOUT TO HISTORY
@app.route('/home/<ObjectId:workout>')
def removeWorkout(workout):
    users = mongo.db.users
    #delete workout from user's active workout
    users.update({ 'username': session['username'] }, { "$pull" : { 'active_workouts' : workout} })
    #add the deleted workout to history
    users.update({ 'username': session['username'] }, {"$push": {'history': workout}} )
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'username' in session:
        #Get user
        users = mongo.db.users
        user = users.find_one({'username': session['username']})
        #Get the user's workouts
        #mdb_user_workouts = user['user_workouts']
        user_workouts = getUserWorkouts(user)
        return render_template('home.html', user_workouts=user_workouts)
    return render_template('index.html')

@app.route('/addexercise', methods=['GET','POST'])
def addexercise():
    #Retrieve user workout data from data base
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    #finding the workout that the user want to add exercise to
    exerciselist = mongo.db.exercises
    workoutlist = mongo.db.workouts
    workcard = workoutlist.find_one({'title': request.form['wtitle'], 'user': session['username']})
    #add the exercise if the workout existed
    if workcard is not None:
        curwork = workcard['_id']
        exerciseid = exerciselist.insert({
            'title' : request.form['etitle'],
            'duration' : request.form['eduration'],
            'link' : request.form['elink']
            })
    #curwork = request.json['workoutId']
        #add the exercise to the workout
        workoutlist.update({'_id': curwork}, { "$push":{ 'exercises' : exerciseid}})
    else:
        flash("Cannot find the workout")

    return redirect(url_for('index'))

@app.route('/addworkout',  methods=['POST'])
def addworkout():
    #Retrieve user workout data from data base
    users = mongo.db.users
    user = users.find_one({'username': session['username']})

    #adding workout to the database and user's workoutlist
    mdb_user_workouts = user['user_workouts']
    workoutlist = mongo.db.workouts
    addw = {
        'title' : request.form['title'],
        'exercises' : [],
        'tags' : request.form['tags'],
        'user' : session['username']
    }
    workid = workoutlist.insert(addw)
    users.update({'username': session['username']}, { "$push":{ 'user_workouts' : workid, 'active_workouts' : workid}})
    return redirect(url_for('index'))

@app.route('/discovery', methods=['GET'])
def discovery():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    friend_discovery_workouts = []
    for friend in user['user_friends']:
        friend_workouts = getUserWorkouts(users.find_one( {'_id': friend} ))
        for fwo in friend_workouts:
            friend_discovery_workouts.append(fwo)
    other_discovery_workouts = []
    db_workouts = []
    for workout in mongo.db.workouts.find():
        db_workouts.append(workout)
    other_discovery_workouts = parseWorkouts(db_workouts, "Lift Discovery", user)
    random.shuffle(other_discovery_workouts)
    #Retrieve user workout data from data base
    return render_template('discovery.html', user_workouts=friend_discovery_workouts, discovery_workouts=other_discovery_workouts)

@app.route('/search', methods=['POST'])
def search():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    search = request.form['search']
    results = searchQuery(search, mongo, user)
    return render_template('search.html', users=results.users, workouts=parseWorkouts(results.workouts, "Lift Workouts", user))

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
                                'user_friends': [],
                                'history': [],
                                'active_workouts': []})
            session['username'] = request.form['username']

            return redirect(url_for('index'))
        errorMessage = 'Username is taken'
        return render_template('register.html', errorMessage=errorMessage)
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
#GET display profile
#POST update profile information

#TODO: split workouts into active and completed workouts
#Display only completed workouts in profile
#Add option to move workout back to active

def profile():
    #Get user
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    image = getProfilePicture(user)

    if request.method == 'POST':
        users.find_one_and_update(
            {'_id': user['_id']},
            {
                '$set': {
                    'name': request.form['name'],
                    'experience': request.form['experience'],
                    'height': request.form['height'],
                    'weight': request.form['weight']
                }
            }
        )

        #Handle file uploading
        if len(request.files) != 0:
            #Check if user has already uploaded a profile photo
            files = mongo.db['fs.files']
            file = files.find_one({'filename': user['username']})

            #Delete current profile image
            if file is not None:
                fileChunks = mongo.db['fs.chunks']
                files.delete_one({'_id': file['_id']})
                fileChunks.delete_one({'files_id': file['_id']})

            #Store profile image
            file = request.files['inputFile']
            mongo.save_file(user['username'], file)

        return redirect(url_for('profile'))

    #Get the user's workouts
    user_workouts = getUserWorkouts(user)
    return render_template('profile.html', user=user, user_workouts=user_workouts, image_data=image)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/handleCheck', methods=['POST'])
def handleCheck():
    #Get workoutId use request.json['workoutId']
    #Get exerciseId user request.json['exerciseId']
    #Get checked status (boolean) of checkbox use request.json['checked']
    print(request.json['checked'])
    return ''

if __name__ == '__main__':
    app.secret_key = key
    app.run(debug=True)
