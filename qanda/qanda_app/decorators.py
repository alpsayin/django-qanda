from models import QandaUser
from django.contrib import auth

def assert_qanda_user(function):
	"""
		Check if QandaUser exists for user and create if not
	"""
	def _decorated(*args, **kwargs):
		user = auth.get_user(args[0])
		if user.is_authenticated():
			if not QandaUser.objects.filter(djangoUser=user).exists():
				QandaUser.objects.create_user(user)
			# print user.QandaUser
		return function(*args, **kwargs)
	return _decorated

def save_object_after(function):
	"""
		Save the model object after computation of the method
	"""
	def _decorated(*args, **kwargs):
		obj = args[0]
		return_value = function(*args, **kwargs)
		obj.save()
		return return_value
	return _decorated