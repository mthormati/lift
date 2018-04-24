class Workout(object):
    title = ""
    exercises = []
    tags = []
    _id = ""
    owner = ""
    image_data = None


def make_workout(title, owner, exercises, tags, _id, image_data):
    workout = Workout()
    workout.title = title
    workout.exercises = exercises
    workout.tags = tags
    workout.owner = owner
    workout._id = _id
    workout.image_data = image_data

    return workout
