from django.conf import settings
from haystack.forms import SearchForm
from models import Question

def search_form(request):
	return {
		'search_form' : SearchForm()
	}

def latest_questions(request):
	return {
		'latest_questions' : Question.objects.all().order_by('-postDate')[:5]
	}

def site_settings(request):
	return {
		'SITE_NAME' : settings.SITE_NAME,
		'ROOT_URL' : settings.ROOT_URL,
		'LOGIN_URL' : settings.LOGIN_URL,
	}