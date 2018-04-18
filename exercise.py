class Exercise(object):
	title = ""
	duration = ""
	link = ""
	relative_id = 0

def make_exercise(title, duration, link, relative_id):
	exercise = Exercise()
	exercise.title = title
	exercise.duration = duration
	exercise.link = link
	exercise.relative_id = relative_id
	return exercise