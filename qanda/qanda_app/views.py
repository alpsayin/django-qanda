# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib import auth
from django.shortcuts import redirect
from django.template.context import RequestContext

from models import *

def get_user(request):
	if not hasattr(request, '_cached_user'):
		request._cached_user = auth.get_user(request)
	return request._cached_user

def index(request):
	return HttpResponse("questions index")

def process_question_relations(request, question, qandaUser):
	if 'star' in request.POST:
		Question.objects.star(qandaUser, question)
	else:
		Question.objects.unstar(qandaUser, question)
	if 'flag' in request.POST:
		Question.objects.flag(qandaUser, question)
	else:
		Question.objects.unflag(qandaUser, question)
	if 'upvote' in request.POST:
		Question.objects.upvote(qandaUser, question)
	else:
		Question.objects.unupvote(qandaUser, question)
	if 'downvote' in request.POST:
		Question.objects.downvote(qandaUser, question)
	else:
		Question.objects.undownvote(qandaUser, question)
	if 'useful' in request.POST:
		Question.objects.useful(qandaUser, question)
	else:
		Question.objects.unuseful(qandaUser, question)
	if 'notUseful' in request.POST:
		Question.objects.notUseful(qandaUser, question)
	else:
		Question.objects.unnotUseful(qandaUser, question)

def process_answer_relations(request, answer, qandaUser):
	if 'star' in request.POST:
		Answer.objects.star(qandaUser, answer)
	else:
		Answer.objects.unstar(qandaUser, answer)
	if 'flag' in request.POST:
		Answer.objects.flag(qandaUser, answer)
	else:
		Answer.objects.unflag(qandaUser, answer)
	if 'upvote' in request.POST:
		Answer.objects.upvote(qandaUser, answer)
	else:
		Answer.objects.unupvote(qandaUser, answer)
	if 'downvote' in request.POST:
		Answer.objects.downvote(qandaUser, answer)
	else:
		Answer.objects.undownvote(qandaUser, answer)
	if 'useful' in request.POST:
		Answer.objects.useful(qandaUser, answer)
	else:
		Answer.objects.unuseful(qandaUser, answer)
	if 'notUseful' in request.POST:
		Answer.objects.notUseful(qandaUser, answer)
	else:
		Answer.objects.unnotUseful(qandaUser, answer)

def process_new_answer(request, question, qandaUser):
	"""
		Process a new answer
	"""
	# print process_new_answer.__doc__
	Answer.objects.create_answer(question, qandaUser, request.POST['answer_text'])

def process_new_reply(request, answer, qandaUser):
	"""
		Process a new reply
	"""
	# print process_new_reply.__doc__
	Reply.objects.create_reply(answer, qandaUser, request.POST['reply_text'])

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

	question.relations = QuestionRelatedUsers.objects.filter(relatedQuestion=question, relatedUser__djangoUser=get_user(request))[0]
	answers = question.answers.filter(deleted=False)
	for answer in answers:
		if AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request)).count():
			answer.relations = AnswerRelatedUsers.objects.filter(relatedAnswer=answer, relatedUser__djangoUser=get_user(request))[0]

	context = {}
	context['question'] = question
	context['answers'] = answers
	context['debug'] = ''
	return render_to_response('question.html', context, context_instance=RequestContext(request))

