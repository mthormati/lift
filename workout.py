class Workout(object):
	_id = ""
	title = ""
	exercises = []
	tags = []


def make_workout(_id, title, exercises, tags):
	workout = Workout()
	workout._id = _id
	workout.title = title
	workout.exercises = exercises
	workout.tags = tags

	return workout
