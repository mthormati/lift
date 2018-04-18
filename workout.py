class Workout(object):
	title = ""
	exercises = []
	tags = []
	relative_id = 0

def make_workout(title, exercises, tags, relative_id):
	workout = Workout()
	workout.title = title
	workout.exercises = exercises
	workout.tags = tags
	workout.relative_id = relative_id
	return workout