class Workout(object):
	#Need to add owner
	title = ""
	owner = ""
	exercises = []
	tags = []


def make_workout(id, title, owner, exercises, tags):
	workout = Workout()
	workout.id = id
	workout.title = title
	workout.owner = owner
	workout.exercises = exercises
	workout.tags = tags

	return workout
