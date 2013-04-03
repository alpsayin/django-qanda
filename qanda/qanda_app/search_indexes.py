import datetime
from haystack.indexes import *
from haystack import site
from models import Question, Answer, Reply

class QuestionIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	title = CharField(model_attr='title')
	author = CharField(model_attr='author')
	postDate = DateTimeField(model_attr='postDate')
	tags = CharField(model_attr='tags')
	answers = CharField(model_attr='answers')
	replies = CharField()

	def get_model(self):
		return Question

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(postDate__lte=datetime.datetime.now(), deleted=False)

	def prepare_author(self, obj):
		return '%s' % obj.author.djangoUser.username

	def prepare_tags(self, obj):
		returnVal = ''
		for tag in obj.tags.all():
			returnVal = returnVal + ' ' + tag.name
		return returnVal

	def prepare_answers(self, obj):
		returnVal = ''
		for answer in obj.answers.all():
			returnVal = returnVal + ' ' + answer.text
		return returnVal

	def prepare_replies(self, obj):
		returnVal = ''
		for answer in obj.answers.all():
			for reply in answer.replies.all():
				returnVal = returnVal + ' ' + reply.text
		return returnVal

site.register(Question, QuestionIndex)
