# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib import auth
from django.shortcuts import redirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from models import *

def get_user(request):
	if not hasattr(request, '_cached_user'):
		request._cached_user = auth.get_user(request)
	return request._cached_user

def index(request):
	return HttpResponseRedirect(reverse(question_page, args=(Question.objects.count(),)))

def process_question_relations(request, question, qandaUser):
	relation_types = ['star', 'flag', 'upvote', 'downvote', 'useful', 'notUseful']
	relations = dict()
	for submitted_key in request.POST:
		if submitted_key in relation_types:
			relations[submitted_key] = True
	for relation_type in relation_types:
		if relation_type not in relations:
			relations[relation_type] = False
	Question.objects.set_relations(qandaUser, question, relations)

def process_answer_relations(request, answer, qandaUser):
	relation_types = ['star', 'flag', 'upvote', 'downvote', 'useful', 'notUseful']
	relations = dict()
	for submitted_key in request.POST:
		if submitted_key in relation_types:
			relations[submitted_key] = True
	for relation_type in relation_types:
		if relation_type not in relations:
			relations[relation_type] = False
	Answer.objects.set_relations(qandaUser, answer, relations)

def process_new_answer(request, question, qandaUser):
	"""
		Process a new answer
	"""
	return Answer.objects.create_answer(qandaUser, question, request.POST['answer_text'])

def process_new_reply(request, answer, qandaUser):
	"""
		Process a new reply
	"""
	return Reply.objects.create_reply(qandaUser, answer, request.POST['reply_text'])

def process_new_question(request, qandaUser):
	"""
		Process a new question
	"""
	return Question.objects.create_question(qandaUser, request.POST['title'], request.POST['question_text'])

def new_question_page(request):
	if request.method == 'POST':
		if request.POST['type'] == 'new_question':
			qandaUser = get_user(request).QandaUser
			question = process_new_question(request, qandaUser)
			return HttpResponseRedirect(reverse(question_page, args=(question.pk,)))
	context = {}
	context['type']='new_question'
	return render_to_response("new_question.html", context, context_instance=RequestContext(request))

def question_page(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	user = get_user(request)
	qandaUser = user.QandaUser

	if request.method == 'POST':
		if request.POST['type'] == 'question' and request.POST['pk'] == str(question.pk):
			process_question_relations(request, question, qandaUser)
		elif request.POST['type'] == 'answer':
			answer = Answer.objects.get(pk=int(request.POST['pk']))
			process_answer_relations(request, answer, qandaUser)
		elif request.POST['type'] == 'new_answer':
			process_new_answer(request, question, qandaUser)
		elif request.POST['type'] == 'new_reply':
			answer = Answer.objects.get(pk=int(request.POST['pk']))
			process_new_reply(request, answer, qandaUser)
		elif request.POST['type'] == 'new_question':
			process_new_question(request, qandaUser)

	all_relations = QuestionRelatedUsers.objects.filter(relatedQuestion=question, relatedUser__djangoUser=get_user(request))
	if all_relations.count() > 0: 
		question.relations = all_relations[0]
	answers = question.answers.filter(deleted=False)
	for answer in answers:
		if AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request)).count():
			answer.relations = AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request))[0]

	context = {}
	context['question'] = question
	context['answers'] = answers
	context['debug'] = ''
	return render_to_response('question.html', context, context_instance=RequestContext(request))

