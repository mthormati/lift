from variables import *
from workout import *
from exercise import *
from flask_pymongo import PyMongo
from __init__ import getProfilePicture
import re

#User object for search result
class SearchedUser(object):
    name = ""
    objId = ""
    isFriend = False
    image_data = None

#Creates searchedUser object
def make_user(name, id, isFriend, image_data):
    searchedUser = SearchedUser()
    searchedUser.name = name
    searchedUser.objId = id
    searchedUser.isFriend = isFriend
    searchedUser.image_data = image_data
    return searchedUser

class SearchResult(object):
    #Users
    users = []
    #Workouts
    workouts = []

#Searches a MDB called "mongo" with the query "search"
def searchQuery(search, mongo, current_user):
    searchResult = SearchResult()
    #Code to find users
    regex = re.compile(".*" + search + ".*", re.IGNORECASE)
    searchedUsers = mongo.db.users.find({"name": regex})
    searchResult.users.clear()
    for user in searchedUsers:
        if (user['_id'] != current_user['_id']): #You cannot search your own profile
            if (user['_id'] not in current_user['user_friends']): #You can only follow users you do not follow already
                searchResult.users.append(make_user(user['name'], user['_id'], True, getProfilePicture(user['username'])))
            else:
                searchResult.users.append(make_user(user['name'], user['_id'], False, getProfilePicture(user['username'])))

    #Code to find workouts
    searchResult.workouts.clear()
    searchedWorkouts = []
    for workout in mongo.db.workouts.find():
        for tag in workout['tags']:
            if search in tag:
                searchedWorkouts.append(workout)
                break

    for workout in searchedWorkouts:
        if (workout['_id'] not in current_user['user_workouts']):
            if (workout['_id'] not in searchResult.workouts):
                searchResult.workouts.append(workout['_id'])
    return searchResult
