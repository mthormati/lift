class Workout(object):
<<<<<<< HEAD
	_id = ""
	title = ""
	exercises = []
	tags = []


def make_workout(_id, title, exercises, tags):
	workout = Workout()
	workout._id = _id
	workout.title = title
	workout.exercises = exercises
	workout.tags = tags

	return workout
=======
    title = ""
    exercises = []
    tags = []
    _id = ""
    owner = ""


def make_workout(title, owner, exercises, tags, _id):
    workout = Workout()
    workout.title = title
    workout.exercises = exercises
    workout.tags = tags
    workout.owner = owner
    workout._id = _id

    return workout
>>>>>>> 5b7d9ffcec465ad325b9051f1c43f5b70a32ebd0
