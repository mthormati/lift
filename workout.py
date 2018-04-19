class Workout(object):
	#Need to add owner
	title = ""
	exercises = []
	tags = []


def make_workout(title, exercises, tags):
	workout = Workout()
	workout.title = title
	workout.exercises = exercises
	workout.tags = tags

	return workout