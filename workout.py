class Workout(object):
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
