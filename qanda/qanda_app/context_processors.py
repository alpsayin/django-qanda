from django.conf import settings
from haystack.forms import SearchForm
from models import Question

def search_form(request):
	return {
		'search_form' : SearchForm()
	}

def latest_questions(request):
	return {
		'latest_questions' : Question.objects.all.order_by('-postDate')[:5]
	}