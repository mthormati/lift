class Exercise(object):
	title = ""
	duration = ""
	link = ""
	key = ""

def make_exercise(title, duration, link, key):
	exercise = Exercise()
	exercise.title = title
	exercise.duration = duration
	exercise.link = link
	exercise.key = key
	return exercise