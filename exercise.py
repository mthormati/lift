class Exercise(object):
	_id = ""
	title = ""
	duration = ""
	link = ""
	key = ""

def make_exercise(_id, title, duration, link, key):
	exercise = Exercise()
	exercise._id = _id
	exercise.title = title
	exercise.duration = duration
	exercise.link = link
	exercise.key = key
	return exercise
