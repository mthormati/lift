class Workout(object):
    title = ""
    exercises = []
    tags = []
    _id = ""


def make_workout(title, exercises, tags, _id):
    workout = Workout()
    workout.title = title
    workout.exercises = exercises
    workout.tags = tags
    workout._id = _id

    return workout