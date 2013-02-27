from django.conf import settings
from haystack.forms import SearchForm
from models import Question
from taggit.models import Tag

NUM_OF_TAGS_IN_COMMON_TAGS = 12
NUM_OF_TAGS_IN_RECENT_TAGS = 12

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

def recent_and_common_tags(request):
	return { 
		'recent_tags' : Tag.objects.order_by('-pk').all()[:NUM_OF_TAGS_IN_RECENT_TAGS],
		'common_tags' : Question.tags.most_common()[:NUM_OF_TAGS_IN_COMMON_TAGS],
	}