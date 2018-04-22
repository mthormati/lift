class Exercise(object):
    title = ""
    duration = ""
    link = ""
    key = ""
    _id = ""

def make_exercise(title, duration, link, key, _id):
    exercise = Exercise()
    exercise.title = title
    exercise.duration = duration
    exercise.link = link
    exercise.key = key
    exercise._id = _id
    return exercise
